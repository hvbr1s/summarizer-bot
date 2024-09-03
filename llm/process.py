import json
import textwrap
from datetime import timedelta
from collections import defaultdict

async def format_time(seconds):
    return str(timedelta(seconds=seconds)).split('.')[0]

async def process_transcription(utterances, transcript_file):
    if isinstance(utterances, str):
        try:
            utterances = json.loads(utterances)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string provided for utterances")

    if not isinstance(utterances, list):
        raise ValueError("Expected utterances to be a list")

    current_speaker = None
    current_start_time = None
    current_end_time = None
    current_text = []

    with open(transcript_file, 'w') as f:
        for utterance in utterances:
            speaker = f"speaker_{utterance['speaker']}"
            start_time = utterance['start']
            end_time = utterance['end']
            text = utterance['text']

            if speaker != current_speaker:
                if current_speaker:
                    # f.write(f"[{await format_time(current_start_time)} - {await format_time(current_end_time)}]\n")
                    f.write(f"<{current_speaker}> {' '.join(current_text)}</{current_speaker}>\n\n")
                current_speaker = speaker
                current_start_time = start_time
                current_end_time = end_time
                current_text = [text]
            else:
                current_end_time = end_time
                current_text.append(text)

        # Write the last speaker's utterance
        if current_speaker:
            # f.write(f"[{await format_time(current_start_time)} - {await format_time(current_end_time)}]\n")
            f.write(f"<{current_speaker}> {' '.join(current_text)}</{current_speaker}>\n\n")

    return transcript_file