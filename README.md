# AI Agent Learning

A small Python app that sends prompts to the Gemini API using the Google GenAI SDK.

## Setup

1. Create and activate a virtual environment if needed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the example environment file and add your real API key:
   ```bash
   copy .env.example .env
   ```
   Then update `.env` with your Gemini key.

## Run the app

```bash
python main.py
```

Then type a question and press Enter. Type `exit` to quit.

## Notes

- The app loads `.env` from the project root automatically.
- The default model is `gemini-3.6-flash`.
