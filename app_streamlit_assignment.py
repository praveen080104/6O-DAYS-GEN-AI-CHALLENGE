import streamlit as st
import json, os
from pathlib import Path

# -----------------------------------------------------------
# STREAMLIT CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="Life Tracker PRO", layout="wide")


# -----------------------------------------------------------
# CSS — square tiles + heading spacing
# -----------------------------------------------------------
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem !important;
        }

        .card {
            background-color:#1e1e1e;
            height: 220px;
            width: 220px;
            border-radius: 22px;
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            border: 2px solid #3c3c3c;
            transition: all 0.25s ease-in-out;
            cursor: pointer;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .card:hover {
            transform: scale(1.10);
            border-color:#a855f7;
            background-color:#2a2a2a;
        }

        a { text-decoration: none !important; color: inherit !important; }

    </style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------
# DATA STORAGE (JSON + image path)
# -----------------------------------------------------------
DATA_FILE = "data.json"
IMG_DIR = Path("images")
IMG_DIR.mkdir(exist_ok=True)


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"username": "", "movies": [], "books": [], "tasks": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


data = load_data()
username = data["username"]
movies = data["movies"]
books = data["books"]
tasks = data["tasks"]


# -----------------------------------------------------------
# PAGE NAVIGATION (LATEST — query_params)
# -----------------------------------------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "home"

query_params = st.query_params
if "page" in query_params:
    st.session_state["page"] = query_params["page"]


def goto(page):
    st.session_state["page"] = page
    st.query_params["page"] = page
    st.rerun()


# -----------------------------------------------------------
# LOGIN PAGE (only first time)
# -----------------------------------------------------------
if username == "":
    st.title("🔐 Login to Life Tracker Pro")
    user = st.text_input("Enter your name:")
    if st.button("Continue ➜"):
        if user.strip():
            data["username"] = user.strip().title()
            save_data(data)
            st.rerun()
    st.stop()


# -----------------------------------------------------------
# HOME PAGE (Square icon buttons)
# -----------------------------------------------------------
if st.session_state["page"] == "home":

    st.markdown(f"""
        <h1 style='text-align:center; font-size:42px; margin-bottom: -10px;'>
        👋 Welcome, {username}
        </h1>
        <h3 style='text-align:center;'>Choose what you want to track</h3>
    """, unsafe_allow_html=True)

    st.write("")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="large")

    with col1:
        st.markdown(f"<a href='/?page=movies' class='card'>🎬<br>Movies</a>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<a href='/?page=books' class='card'>📚<br>Books</a>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<a href='/?page=tasks' class='card'>✅<br>Tasks</a>", unsafe_allow_html=True)

    with col4:
        st.markdown(f"<a href='/?page=dashboard' class='card'>📊<br>Dashboard</a>", unsafe_allow_html=True)


# -----------------------------------------------------------
# MOVIES PAGE
# -----------------------------------------------------------
elif st.session_state["page"] == "movies":

    st.markdown("<h1 style='text-align:center;'>🎬 Movies Watched</h1>", unsafe_allow_html=True)

    if st.button("⬅ Back"):
        goto("home")

    col = st.columns([1, 2, 1])[1]
    with col:
        name = st.text_input("Movie name:", placeholder="Enter movie name...")
        poster = st.file_uploader("Upload poster", type=["jpg", "jpeg", "png"])

        if st.button("Add Movie"):
            if name and poster:
                path = IMG_DIR / f"movie_{name}.jpg"
                with open(path, "wb") as f:
                    f.write(poster.read())
                movies.append({"name": name, "image": str(path)})
                save_data(data)
                st.success("✅ Movie added!")
                st.rerun()

    st.write("### Your Movies:")
    for m in movies:
        st.image(m["image"], width=130)
        st.write(f"🎬 **{m['name']}**")
        st.write("---")


# -----------------------------------------------------------
# BOOKS PAGE
# -----------------------------------------------------------
elif st.session_state["page"] == "books":

    st.markdown("<h1 style='text-align:center;'>📚 Books Reading</h1>", unsafe_allow_html=True)

    if st.button("⬅ Back"):
        goto("home")

    col = st.columns([1, 2, 1])[1]
    with col:
        name = st.text_input("Book name:", placeholder="Enter book name...")
        cover = st.file_uploader("Upload cover", type=["jpg", "jpeg", "png"])

        if st.button("Add Book"):
            if name and cover:
                path = IMG_DIR / f"book_{name}.jpg"
                with open(path, "wb") as f:
                    f.write(cover.read())
                books.append({"name": name, "image": str(path)})
                save_data(data)
                st.success("✅ Book added!")
                st.rerun()

    st.write("### Your Books:")
    for b in books:
        st.image(b["image"], width=130)
        st.write(f"📘 **{b['name']}**")
        st.write("---")


# -----------------------------------------------------------
# TASK PAGE
# -----------------------------------------------------------
elif st.session_state["page"] == "tasks":

    st.markdown("<h1 style='text-align:center;'>✅ Daily Tasks</h1>", unsafe_allow_html=True)

    if st.button("⬅ Back"):
        goto("home")

    col = st.columns([1, 2, 1])[1]
    with col:
        task = st.text_input("Add a task:", placeholder="Enter task...")

        if st.button("Add Task"):
            if task:
                tasks.append({"task": task, "done": False})
                save_data(data)
                st.rerun()

    st.write("### Tasks:")
    for i, t in enumerate(tasks):
        left, right = st.columns([6, 1])
        left.write(f"- {t['task']}")
        if right.checkbox("Done", t["done"], key=f"task_{i}"):
            t["done"] = True
            save_data(data)


# -----------------------------------------------------------
# DASHBOARD PAGE
# -----------------------------------------------------------
elif st.session_state["page"] == "dashboard":

    st.markdown("<h1 style='text-align:center;'>📊 Dashboard</h1>", unsafe_allow_html=True)

    if st.button("⬅ Back"):
        goto("home")

    st.metric("🎬 Movies Watched", len(movies))
    st.metric("📚 Books Added", len(books))
    st.metric("✅ Tasks Today", len(tasks))
