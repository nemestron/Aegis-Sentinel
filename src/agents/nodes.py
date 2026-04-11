"""
Filtering, Authentication, Synthesis & Formatting Personas
Author: Dhiraj Malwade
"""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from src.state import AgentState
from src.memory.vector_store import search_memory

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize LLMs with the requested fallback strategy
def get_llm(primary_model: str):
    fallback_model = "llama-3.3-70b-versatile"
    primary = ChatGroq(model=primary_model, temperature=0.1, api_key=groq_api_key)
    fallback = ChatGroq(model=fallback_model, temperature=0.1, api_key=groq_api_key)
    return primary.with_fallbacks([fallback])

# Define the models exactly as requested in the documentation
triage_llm = get_llm("llama-3.1-8b-instant")
auth_llm = get_llm("meta-llama/llama-4-maverick-17b-128e-instruct")
synth_llm = get_llm("deepseek-r1-distill-qwen-32b")
format_llm = get_llm("llama-3.1-8b-instant")

def triage_node(state: AgentState) -> dict:
    """Filters noise and extracts relevant financial data."""
    prompt = PromptTemplate.from_template(
        "Analyze the following raw financial data. Extract and summarize only the highly relevant financial information for the ticker {ticker}. Filter out all noise and generic text.\n\nRaw Data: {raw_data}"
    )
    chain = prompt | triage_llm
    result = chain.invoke({"ticker": state.ticker, "raw_data": state.raw_data})
    return {"raw_data": result.content}

def auth_node(state: AgentState) -> dict:
    """Verifies facts against ChromaDB context, isolated by ticker to prevent cross-contamination."""
    # Ensure retrieval is strictly locked to the state.ticker
    results = search_memory(state.ticker, ticker=state.ticker, n_results=6)
    docs = results.get('documents', [[]])[0]
    metas = results.get('metadatas', [[]])[0]
    
    if not docs:
        return {"verified": False, "retrieved_docs": [], "source_links": []}

    source_links = list(set([m.get("source", "") for m in metas if m.get("source")]))
    context = "\n\n".join(docs)
    
    prompt = PromptTemplate.from_template(
        "You are a strict fact-checker. Verify the following Data against the provided Context. Is the Data fundamentally supported by the Context? Respond with EXACTLY 'TRUE' or 'FALSE' and nothing else.\n\nData: {data}\n\nContext: {context}"
    )
    chain = prompt | auth_llm
    result = chain.invoke({"data": state.raw_data, "context": context})
    
    is_verified = "TRUE" in result.content.upper()
    
    return {
        "verified": is_verified,
        "retrieved_docs": docs,
        "source_links": source_links
    }

def synthesis_node(state: AgentState) -> dict:
    """Rewrites verified intelligence into a concise, insightful brief."""
    if not state.verified:
        return {"final_brief": "CRITICAL: The intelligence gathered could not be independently authenticated against the vector memory. No brief generated."}
        
    context = "\n".join(state.retrieved_docs)
    prompt = PromptTemplate.from_template(
        "Based STRICTLY on the following Verified Data and Context, write a concise, insightful 2-3 line financial brief for {ticker}. Do not invent any information.\n\nVerified Data: {raw_data}\n\nContext: {context}"
    )
    chain = prompt | synth_llm
    result = chain.invoke({"ticker": state.ticker, "raw_data": state.raw_data, "context": context})
    return {"final_brief": result.content}

def formatting_node(state: AgentState) -> dict:
    """Structures output with specific Markdown formatting and source links."""
    links_str = "\n".join([f"- {link}" for link in state.source_links])
    prompt = PromptTemplate.from_template(
        "Format the following financial brief into clean, professional Markdown. Add a clear header. Add a section titled 'Sources' and list the provided links as Markdown bullet points. Do not change the core information.\n\nBrief: {brief}\n\nSources:\n{links}"
    )
    chain = prompt | format_llm
    result = chain.invoke({"brief": state.final_brief, "links": links_str})
    return {"final_brief": result.content}