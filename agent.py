from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import SecretStr
import os
from dotenv import load_dotenv
import logging
import asyncio
import io

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(api_key)

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-flash-exp', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))

agent = Agent(
    task="Navigate to onlyfans.com and extract the text of the website privacy policy",
    llm=llm
)

async def monitor_logs(log_stream):
    last_position = 0
    
    while True:
        current_position = log_stream.tell()
        
        log_stream.seek(last_position)
        new_content = log_stream.read()
        
        last_position = log_stream.tell()
        
        if new_content:
            print(f"New log content: {new_content}")
        
        await asyncio.sleep(0.1)

async def main(stream):
    log_stream = io.StringIO()
    new_handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger('browser_use')
    logger.setLevel(logging.INFO)
    new_handler.setLevel(logging.INFO)
    logger.addHandler(new_handler)
    logger.info("Starting agent")
 
    monitor_task = asyncio.create_task(monitor_logs(log_stream))
    agent_task = asyncio.create_task(agent.run())
    
    await agent_task
    
    monitor_task.cancel()
    try:
        await monitor_task
    except asyncio.CancelledError:
        pass

import asyncio

if __name__ == "__main__":
    asyncio.run(main())