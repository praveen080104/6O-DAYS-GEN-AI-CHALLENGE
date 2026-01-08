from playwright.sync_api import sync_playwright
import pandas as pd
import time

def scrape_batting_rows():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("🌐 Searching DuckDuckGo")
        page.goto("https://duckduckgo.com", timeout=0)

        page.locator("input[name='q']").fill("india vs south africa womens final cricbuzz scorecard")
        page.locator("input[name='q']").press("Enter")

        page.wait_for_selector("a[data-testid='result-title-a']")
        link = page.locator("a[data-testid='result-title-a']").first
        print(f"🔗 Opening: {link.inner_text()}")
        link.click()

        page.wait_for_load_state("domcontentloaded")
        time.sleep(1.5)

        print("➡ Clicking Scorecard tab...")

        page.evaluate("""() => {
            const nav = document.querySelector('#main-nav');
            if (nav) nav.scrollLeft = nav.scrollWidth;
        }""")

        page.locator('xpath=//*[@id="main-nav"]/a[contains(text(), "Scorecard")]').click(force=True)
        time.sleep(2)  # wait for scorecard to load

        print("📊 Extracting batting rows...")

        # ✅ Your DIV container XPath (NO TABLES - ALL DIV BASED DATA)
        BATSMAN_DIV_XPATH = '/html/body/div[1]/main/div/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[1]/div'

        # ✅ Get all batting rows under this block
        rows = page.locator(f'xpath={BATSMAN_DIV_XPATH}').locator("div")

        print("✅ Total div row blocks detected:", rows.count())

        batting_data = []

        for i in range(rows.count()):
            row = rows.nth(i)

            # each batting line is inside nested divs
            cols = row.locator("div")

            if cols.count() < 7:
                continue  # skip rows that don’t have full batting columns

            player = cols.nth(0).inner_text().strip()
            dismissal = cols.nth(1).inner_text().strip()
            runs   = cols.nth(2).inner_text().strip()
            balls  = cols.nth(3).inner_text().strip()
            fours  = cols.nth(4).inner_text().strip()
            sixes  = cols.nth(5).inner_text().strip()
            sr     = cols.nth(6).inner_text().strip()

            # skip headers like ("R", "B", "4s") etc.
            if not runs.isdigit():
                continue

            batting_data.append([player, dismissal, runs, balls, fours, sixes, sr])

        if not batting_data:
            print("\n❌ No batting data found — the XPath might need to be inspected again.")
            browser.close()
            return

        df = pd.DataFrame(
            batting_data,
            columns=["Player", "Dismissal", "Runs", "Balls", "4s", "6s", "SR"]
        )
        df.to_excel("cricbuzz_batting_scores.xlsx", index=False)

        print("\n✅ SUCCESS: Batting scores saved to: cricbuzz_batting_scores.xlsx")

        browser.close()


if __name__ == "__main__":
    scrape_batting_rows()

