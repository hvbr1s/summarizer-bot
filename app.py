import os
import aiohttp
import asyncio
from dotenv import load_dotenv
from llm.call import summarize
from llm.process import process_transcription

# Initialize environment variables
load_dotenv()

PROJECT_NAME = input("👋 Welcome! Please enter the project name: ").strip().lower()
speakers = input("🌐 Great! How many speakers took part in the call: ").strip().lower()
SPEAKERS = int(speakers)

# Load Audio File
AUDIO_FILE = './audio_file/meeting.mp3'

# Load API keys
GLADIA_KEY = os.environ['GLADIA_KEY']

async def upload_audio(file_path):
    url = "https://api.gladia.io/v2/upload"
    headers = {
        'x-gladia-key': GLADIA_KEY,
    }
    file_full_path = os.path.abspath(file_path)
    print(f"Uploading audio file from path: {file_full_path}")
    
    try:
        async with aiohttp.ClientSession() as session:
            with open(file_full_path, 'rb') as audio_file:
                data = aiohttp.FormData()
                data.add_field('audio', audio_file, filename=os.path.basename(file_full_path))
                async with session.post(url, headers=headers, data=data) as response:
                    response.raise_for_status()  
                    return await response.json()
    except FileNotFoundError:
        print(f"File not found: {file_full_path}")
        raise
    except Exception as e:
        print(f"An error occurred while uploading audio: {e}")
        raise

async def get_transcription(audio_url):
    headers = {
        "x-gladia-key": GLADIA_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "context_prompt": "This is the transcript of a meeting between the Certora team and a client team regarding a security audit.",
        "language": "en",
        "diarization": True,
        "diarization_config": {
            "min_speakers": 2,
            "max_speakers": SPEAKERS
        },
        "audio_url": audio_url
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.gladia.io/v2/transcription/", headers=headers, json=data) as response:
            response.raise_for_status()
            response_data = await response.json()
            
            result_url = response_data.get("result_url")
            if not result_url:
                raise ValueError("Result URL is missing in the transcription response.")
            
        print("Transcription in progress...", end="", flush=True)
        progress_dots = ""
        while True:
            async with session.get(result_url, headers=headers) as poll_response:
                poll_response.raise_for_status()
                poll_data = await poll_response.json()
                if poll_data.get("status") == "done":
                    print("\033[K\nTranscription complete!")
                    # Extract the relevant transcription data
                    transcription = poll_data.get("result", {}).get("transcription", {})
                    utterances = transcription.get("utterances", [])
                    return utterances
                else:
                    progress_dots += "."
                    print(f"\rTranscription in progress...{progress_dots}", end="", flush=True)
                    await asyncio.sleep(1)

async def main():   
    # Define output file
    output_folder = f'./calls/{PROJECT_NAME}/'
    summary_file = f'{output_folder}{PROJECT_NAME}_summary.txt'
    transcript_file = f'{output_folder}{PROJECT_NAME}_transcript.txt'
    
    # Check if the output folder exists, if not create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder} 📁")
    
    # Upload audio and get transcription
    upload_response = await upload_audio(AUDIO_FILE)
    audio_url = upload_response.get("audio_url")
    print(f'Job URL: {audio_url}')
    if not audio_url:
        raise ValueError("Audio URL is missing in the upload response.")
    
    utterances = await get_transcription(audio_url)
    await process_transcription(utterances, transcript_file)
    print(f"Transcript has been written to {transcript_file}💾✅")
    
    # Read the content of the transcript file
    with open(transcript_file, 'r') as file:
        transcript_content = file.read()  
    
    summary = await summarize(transcript_content, PROJECT_NAME.capitalize())
    with open(summary_file, 'w') as tx_file:
        tx_file.write(summary)
    print(f"Summary has been written to {summary_file}💾✅")
    
# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())