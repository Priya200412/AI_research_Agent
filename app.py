import streamlit as st
import wikipedia
from duckduckgo_search import DDGS
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API Key
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Check API key
if not api_key:
    st.error("OPENAI_API_KEY not found in .env file")
    st.stop()

client = OpenAI(api_key=api_key)

st.title("AI Research Agent")
st.subheader("Generative AI Based Research Assistant")

# User Input
query = st.text_input("Enter Research Topic")

# Search Web Function
def search_web(query):
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(r["body"])
    except Exception as e:
        st.error(f"Web search error: {e}")
    return " ".join(results)


# AI Summary Function
def generate_summary(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful research assistant."},
                {"role": "user", "content": f"Summarize this:\n{text}"}
            ],
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"


# Button Click
if st.button("Generate Research"):

    if not query:
        st.warning("Please enter a research topic")
        st.stop()

    st.write("Collecting Research Data...")

    # Wikipedia Data
    try:
        wiki_data = wikipedia.summary(query, sentences=5)
    except Exception as e:
        wiki_data = "No Wikipedia Data Found"

    # Web Search
    web_data = search_web(query)

    combined_data = wiki_data + " " + web_data

    st.write("Generating AI Summary...")

    summary = generate_summary(combined_data)

    st.subheader("Research Summary")
    st.write(summary)

    st.subheader("Wikipedia Data")
    st.write(wiki_data)