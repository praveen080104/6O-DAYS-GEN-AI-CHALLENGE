from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    greeting = None

    if request.method == "POST":
        name = request.form.get("name")
        age = int(request.form.get("age"))

        if age < 18:
            greeting = f"Hey {name}! You're young and full of energy! 🚀"
        elif 18 <= age <= 40:
            greeting = f"Hello {name}! You're in your prime — keep hustling! 💼✨"
        else:
            greeting = f"Hi {name}! Wisdom suits you brilliantly. 🌟"

    return render_template("index.html", greeting=greeting)

if __name__ == "__main__":
    app.run(debug=True)
