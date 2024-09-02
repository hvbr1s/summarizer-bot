# Call Summarizer App

This application transcribes and summarizes audio recordings of meetings or calls.

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv venvsummarizer
   source venvsummarizer/bin/activate 
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create required directories:
   ```
   mkdir calls audio_file
   ```

5. Add your audio file:
   - Place your audio file (named `meeting_recording.mp3`) in the `audio_file` directory.

6. Set up environment variables:
   - Create a `.env` file in the project root.
   - Add your Gladia API key:
     ```
     GLADIA_KEY=your_gladia_api_key_here
     ```

## Usage

Run the main script:

```
make app
```

Follow the prompts to enter the project name and number of speakers.

The script will process the audio file and generate a summary in the `calls/<project_name>/` directory.

## Notes

- Ensure your audio file is in MP3 format and named `meeting.mp3`.
- The summary will be saved as a Markdown file in the `calls/<project_name>/` directory.