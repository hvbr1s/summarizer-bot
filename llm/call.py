import os
import math
import json
from dotenv import load_dotenv
from llm.prompt import prepare_prompt
from anthropic import AsyncAnthropic

# Initialize environment variables
load_dotenv()

# Set up OpenAI
claude_client = AsyncAnthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
claude_model_prod = "claude-3-5-sonnet-20240620"

# Function to prepare a summary
async def summarize(summary, project_name):
    try:

        prompt = await prepare_prompt(project_name, summary)
        response = await claude_client.messages.create(
            temperature=0.0,
            model=claude_model_prod,
            system="You are a specialized summarization AI focused on extracting key security audit details from meeting transcripts between Certora and client teams.",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=	8192
        )
        schedule = response.content[0].text
        return schedule
    except Exception as e:
        print(e)
        return("Oops, I wasn't able to summarize this call")