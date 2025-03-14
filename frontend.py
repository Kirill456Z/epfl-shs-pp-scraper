import streamlit as st
import time  # For demonstration purposes
from agent import main
import asyncio

st.title("Privacy Policy Scraper")

DEFAULT_PROMPT = "Navigate to {website_url} and find the privacy policy page. Return the url of the page."

api_key = st.text_input("API key", value="")
website_url = st.text_input("Website url", value="onlyfans.com")
agent_prompt = st.text_input("Agent prompt", value=DEFAULT_PROMPT)

output_container = st.empty()

class StreamHandler:
    def __init__(self, container):
        self.container = container
        self.text = ""
    
    def write(self, text):
        self.text += text
        self.container.markdown(f"```\n{self.text}\n```")

# Button to process inputs
if st.button("Compute"):
    stream = StreamHandler(output_container)

    result = asyncio.run(main(stream, website_url, agent_prompt, api_key))

    if result.is_done():
        st.success(result.final_result())
    else:
        st.error(result.errors())
