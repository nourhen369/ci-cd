import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Utility Hub", layout="wide")

st.title("Utility Hub — Task Manager & Notepad")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "notes" not in st.session_state:
    st.session_state.notes = ""

page = st.sidebar.radio("Navigation", ["Task Manager", "Notepad", "Dashboard"])

if page == "Task Manager":
    st.header("📋 Task Manager")

    with st.form("add_task"):
        task_text = st.text_input("New task")
        due_date = st.date_input("Due date", value=None)
        submitted = st.form_submit_button("Add Task")
        if submitted and task_text.strip():
            st.session_state.tasks.append({
                "task": task_text.strip(),
                "due": due_date if due_date else "No date",
                "done": False,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

    if st.session_state.tasks:
        st.subheader("Your Tasks")
        for i, t in enumerate(st.session_state.tasks):
            cols = st.columns([0.1, 0.6, 0.3, 0.2])
            with cols[0]:
                if st.checkbox("", value=t["done"], key=f"done_{i}"):
                    t["done"] = True
            with cols[1]:
                st.write(f"**{t['task']}**")
            with cols[2]:
                st.caption(f"Due: {t['due']}")
            with cols[3]:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.tasks.pop(i)
                    st.experimental_rerun()
    else:
        st.info("No tasks yet.")

elif page == "Notepad":
    st.header("📝 Notepad")
    st.session_state.notes = st.text_area("Write your notes here:", value=st.session_state.notes, height=350)
    st.success("Notes saved automatically.")

elif page == "Dashboard":
    st.header("📊 Dashboard")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Task Status")
        if st.session_state.tasks:
            df = pd.DataFrame(st.session_state.tasks)
            df["status"] = df["done"].map({True: "Done", False: "Pending"})
            st.bar_chart(df["status"].value_counts())
        else:
            st.info("No data to display.")

    with col2:
        st.subheader("Notes Length")
        st.metric("Characters", len(st.session_state.notes))

st.markdown("---")
st.caption("A simple visual Streamlit app with a task manager and notepad.")