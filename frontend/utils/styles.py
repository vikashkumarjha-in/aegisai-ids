import streamlit as st


def load_css():

    st.markdown(
        """
        <style>

        .main {
            background-color: #0b1220;
            color: white;
        }

        .stMetric {
            background-color: #111827;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #1f2937;
        }

        .block-container {
            padding-top: 2rem;
        }

        h1, h2, h3 {
            color: #f9fafb;
        }

        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }

        </style>
        """,
        unsafe_allow_html=True
    )