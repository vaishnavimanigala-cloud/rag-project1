import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>
            :root {
                --bg: #0f172a;
                --panel: #111827;
                --card: #1f2937;
                --primary: #38bdf8;
                --accent: #a78bfa;
                --muted: #94a3b8;
                --success: #22c55e;
                --warning: #fbbf24;
                --danger: #ef4444;
                --text: #e2e8f0;
            }

            .stApp {
                background: linear-gradient(180deg, #020817 0%, #0f172a 100%);
                color: var(--text);
            }

            h1, h2, h3, h4, h5 {
                color: #f8fafc;
            }

            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 2rem;
            }

            div[data-testid="stFileUploader"] {
                background: rgba(15, 23, 42, 0.9);
                border-radius: 12px;
                padding: 0.5rem;
            }

            .stAlert {
                border-radius: 12px;
            }

            .metric-card {
                background: rgba(31, 41, 55, 0.9);
                padding: 1rem;
                border-radius: 12px;
                border: 1px solid rgba(148, 163, 184, 0.2);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
