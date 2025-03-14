from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import SecretStr
import os
from dotenv import load_dotenv
import logging
import asyncio
import io
from string import Formatter
from browser_use import BrowserConfig, Browser

config = BrowserConfig(
    headless=True
)

browser = Browser(config=config)

load_dotenv()

class StreamLogHandler(logging.Handler):
    def __init__(self, stream_handler):
        super().__init__()
        self.stream_handler = stream_handler
    
    def emit(self, record):
        log_message = self.format(record)
        self.stream_handler.write(log_message + "\n")

async def main(stream_handler, website_url, agent_prompt, api_key):
    keys = {k for _, k, _, _ in Formatter().parse(agent_prompt) if k}
    if "website_url" not in keys:
        stream_handler.write("Could not format prompt with a website url.\n\nEnsure the prompt contains placeholder {website_url}")
        raise ValueError("Could not format prompt with a website url")

    full_prompt = agent_prompt.format(website_url=website_url)
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=api_key)
    agent = Agent(
        browser=browser,
        task=full_prompt,
        llm=llm
    )

    log_handler = StreamLogHandler(stream_handler)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    
    logger = logging.getLogger('browser_use')
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    
    result = await agent.run()
    
    logger.removeHandler(log_handler)
    return result
