"""Interface métier de RegRAG (Streamlit).

Phase 0 : affiche l'état du système. Phase 2 : questions, réponses, citations
cliquables et pouce haut/bas pour le feedback.
"""

import os

import httpx
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="RegRAG", page_icon="📚", layout="wide")
st.title("RegRAG")
st.caption(
    "Assistant sur les textes réglementaires IA et assurance. "
    "Vous échangez avec une IA ; ses réponses ne constituent pas un avis juridique."
)

with st.sidebar:
    st.subheader("État du système")
    try:
        report = httpx.get(f"{API_URL}/health", timeout=5).json()
        st.write(f"Global : **{report['status']}** · v{report.get('version', '?')}")
        for dep in report["dependencies"]:
            icon = "🟢" if dep["status"] == "ok" else "🔴"
            st.write(f"{icon} {dep['name']} — {dep['latency_ms']} ms")
    except Exception as exc:  # noqa: BLE001
        st.error(f"API injoignable : {exc}")

question = st.text_input("Votre question", placeholder="Que dit l'article 50 de l'AI Act ?")
if st.button("Demander", disabled=not question):
    resp = httpx.post(f"{API_URL}/ask", json={"question": question}, timeout=60)
    if resp.status_code == 501:
        st.info("La génération de réponses arrive en phase 2.")
    else:
        st.json(resp.json())
