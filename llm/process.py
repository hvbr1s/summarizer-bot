import textwrap
from collections import defaultdict

async def process_transcription(poll_data):
    utterances = poll_data['result']['transcription']['utterances']
    speakers = defaultdict(list)
    
    for utterance in utterances:
        speaker = f"speaker_{utterance['speaker'] + 1}"  # Adding 1 to start from speaker_1
        text = utterance['text'].strip()
        
        # Capitalize the first letter of each sentence
        text = '. '.join(sentence.capitalize() for sentence in text.split('. '))
        
        # If the previous utterance for this speaker ends with a comma or doesn't end with punctuation,
        # append this utterance to it instead of creating a new one
        if speakers[speaker] and (speakers[speaker][-1].endswith(',') or not speakers[speaker][-1][-1] in '.!?'):
            speakers[speaker][-1] += ' ' + text
        else:
            speakers[speaker].append(text)
    
    conversation = []
    for speaker, texts in speakers.items():
        conversation.append(f"<{speaker}>")
        for text in texts:
            # Split long lines
            wrapped_text = textwrap.fill(text, width=80, initial_indent='  ', subsequent_indent='    ')
            conversation.append(wrapped_text)
        conversation.append(f"</{speaker}>")
        conversation.append("")  # Add a blank line between speakers
    
    return "\n".join(conversation)