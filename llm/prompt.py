async def prepare_prompt(project_name, transcript):
    try:
        
        SUMMARIZER = f'''
You are tasked with summarizing a transcript of a meeting between the Certora team and the {project_name} team regarding a security audit. The audit will be performed by Certora, and {{project_name}} is the client. 

Your goal is to provide a clear and concise summary of the meeting, focusing on the main security concerns and the areas of focus for both manual code review and formal verification.

First, carefully read and analyze the following transcript:

<transcript>
{transcript}
</transcript>

After analyzing the transcript, summarize the meeting by following these guidelines:

<thinking>
1. Identify the main security concerns expressed by the {project_name} team.
2. Determine the areas of focus for the manual code review.
3. Identify the aspects that should be prioritized for formal verification using the Certora Prover.
4. Note any specific requests or concerns raised by either team.
5. Highlight any agreed-upon next steps or action items.
<thinking>

Present your summary in text format, using appropriate headings, bullet points, and formatting to ensure clarity and readability. Structure your summary as follows:

1. Brief introduction
2. Main security concerns
3. Focus areas for manual code review
4. Priorities for formal verification
5. Additional notes or action items

Remember to think step by step as you analyze the transcript and formulate your summary. Consider the context of a security audit and the two-part process involving manual code review and formal verification.
Begin your response now.
   
'''    
        return SUMMARIZER
    except Exception as e:
      print(e)
      return SUMMARIZER