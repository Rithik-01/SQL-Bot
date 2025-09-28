import streamlit as st
from tools.db_connection import get_tables,get_columns
from config import DB_NAME
from streamlit_mic_recorder import speech_to_text
from agent import agent
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="NL → SQL Bot", layout="wide")

st.title("Natural Language → SQL Bot")
st.write(f"Connected to database: **{DB_NAME}**")

st.sidebar.header("📂 Schema Explorer")

tables = get_tables()
if tables:
    selected_table = st.sidebar.selectbox("Select a table", tables)

    if selected_table:
        columns = get_columns(selected_table)
        st.sidebar.write("**Columns:**")
        for col in columns:
            st.sidebar.markdown(f"- {col}")
else:
    st.sidebar.warning("No tables found in this database.")


if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

st.subheader("Enter your command")

typed_input = st.text_area(
    "",
    width=800,
    placeholder="e.g., Add a column called age to the users table"
)

# st.subheader("Speak your command")

voice_text = speech_to_text(
    language='en',
    start_prompt="🎙️",
    stop_prompt="⏹️",
    use_container_width=False,
    just_once=True,
    key='stt'
)
print(voice_text)

if voice_text:
    st.session_state["user_input"] = voice_text
    st.info(f"🗣️ You said: {voice_text}")
elif typed_input.strip():
    st.session_state["user_input"] = typed_input


if st.button("Execute"):
    if st.session_state["user_input"].strip():
        try:
            result,visualize = agent(st.session_state["user_input"])

            if visualize=='no':
                st.success("✅ Query executed successfully. Result available.",width=400)
                if result is not None and not result.empty:
                    st.dataframe(result)
            else:
                st.success("✅ Query executed successfully. Result available.",width=400)
                st.pyplot(result,width=700)

        except Exception as e:
            st.error(f"❌ Error: {e}")

    else:
        st.warning("Please enter an instruction.")