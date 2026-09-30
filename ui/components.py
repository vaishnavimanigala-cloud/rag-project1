import streamlit as st


def status_badge(label, active):
    color = "#22c55e" if active else "#ef4444"
    st.markdown(
        f"<span style='display:inline-block; padding:6px 12px; border-radius:999px; background:{color}; color:white; font-size:0.8rem; font-weight:700; margin-right:10px;'>{label}</span>",
        unsafe_allow_html=True,
    )
