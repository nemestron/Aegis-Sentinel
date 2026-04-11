"""
Aegis Sentinel - Command Dashboard
Author: Dhiraj Malwade
"""
import streamlit as st
import time
from concurrent.futures import ThreadPoolExecutor
from fpdf import FPDF
import os
import re
from dotenv import load_dotenv

from src.graph_engine import invoke_graph_autonomous
from src.delivery.transmission import send_telegram_message

# Ensure environment variables are loaded securely
load_dotenv()

st.set_page_config(page_title="Aegis Sentinel", layout="centered")

class PDFReport(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 16)
        self.cell(0, 10, "Aegis Sentinel Intelligence Report", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(state_data: dict) -> bytes:
    """Generates a downloadable PDF from the state data."""
    pdf = PDFReport()
    pdf.add_page()
    
    ticker = state_data.get("ticker", "UNKNOWN")
    company = state_data.get("company_name") or ticker
    price = state_data.get("current_price", "N/A")
    change = state_data.get("change_percent", "N/A")
    verified = state_data.get("verified", False)
    brief = state_data.get("final_brief", "No brief available.")
    sources = state_data.get("source_links", [])

    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, f"Target: {company} ({ticker})", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 10, f"Current Price: {price}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"24h Change: {change}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Verification Status: {'VERIFIED' if verified else 'UNVERIFIED'}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Intelligence Brief:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=11)
    
    # Strip markdown symbols for clean PDF rendering
    clean_brief = re.sub(r'[*_#`]', '', brief)
    pdf.multi_cell(0, 6, clean_brief)
    pdf.ln(5)

    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Sources:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=10)
    pdf.set_text_color(0, 0, 255)
    for link in sources:
        pdf.cell(0, 6, link, link=link, new_x="LMARGIN", new_y="NEXT")

    # fpdf2 output() returns a bytearray
    return bytes(pdf.output())

# UI Layout
st.title("Aegis Sentinel Command Dashboard")
st.markdown("Autonomous Financial Intelligence & Cryptographic Verification System")

# State Management for Thread Isolation
if "executor" not in st.session_state:
    st.session_state.executor = ThreadPoolExecutor(max_workers=1)
if "future" not in st.session_state:
    st.session_state.future = None
if "result" not in st.session_state:
    st.session_state.result = None

ticker_input = st.text_input("Enter Target Ticker Symbol (e.g., RELIANCE.NS, AAPL, BARC.L):").strip().upper()

if st.button("Run Analysis"):
    if not ticker_input:
        st.warning("Please enter a valid ticker symbol.")
    else:
        st.session_state.result = None
        # Dispatch the blocking graph execution to the background thread
        st.session_state.future = st.session_state.executor.submit(invoke_graph_autonomous, ticker_input)

# Polling Mechanism
if st.session_state.future and not st.session_state.future.done():
    with st.status("Acquiring Intelligence & Authenticating... Please wait.", expanded=True) as status:
        st.write("Traversing Cognitive Graph...")
        time.sleep(1.5)
        st.rerun()

# Thread Resolution
if st.session_state.future and st.session_state.future.done() and not st.session_state.result:
    try:
        st.session_state.result = st.session_state.future.result()
    except Exception as e:
        st.error(f"Pipeline Execution Failed: {e}")
    finally:
        st.session_state.future = None

# Results Display
if st.session_state.result:
    state = st.session_state.result
    st.success("Intelligence Acquisition Complete.")

    st.subheader(f"Target: {state.get('company_name') or state.get('ticker')}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", state.get("current_price"))
    col2.metric("24h Change", state.get("change_percent"))
    col3.metric("Authentication", "VERIFIED" if state.get("verified") else "UNVERIFIED")

    st.markdown("### Executive Brief")
    st.markdown(state.get("final_brief"))

    st.markdown("### Sources")
    for link in state.get("source_links", []):
        st.markdown(f"- [{link}]({link})")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        pdf_bytes = generate_pdf(state)
        st.download_button(
            label="Download as PDF",
            data=pdf_bytes,
            file_name=f"{state.get('ticker')}_Aegis_Report.pdf",
            mime="application/pdf"
        )

    with col_b:
        if st.button("Send to Telegram"):
            message = f"*AEGIS INTELLIGENCE: {state.get('company_name') or state.get('ticker')}*\n"
            message += f"Current Price: {state.get('current_price')}\n"
            message += f"24h Change: {state.get('change_percent')}\n"
            message += f"Authentication: {'VERIFIED' if state.get('verified') else 'UNVERIFIED'}\n\n"
            message += f"{state.get('final_brief')}"
            
            success = send_telegram_message(message)
            if success:
                st.success("Report transmitted successfully.")
            else:
                st.error("Transmission failed. Check application logs.")