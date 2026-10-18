# Cecilia

An AI powered tool to talk and work with you! (Inspired by jarvis btw)

## API

Access the route /scalar or /docs for the complete routes, where you can test or see what something do.

## Instalation

- Install the repo with: `git clone https://github.com/GF-Silva/Cecilia`
- Install python and uv
- and run:

``` bash
cd Cecilia
uv venv
source .venv/bin/activate
uv sync
uv run uvicorn cecilia.main:app --reload
```

- You will be able to access at localhost:8000
- Notice that it is still just backend, so the only routes are API routes wich you can see at localhost:8000/scalar

## Features

The project integrates with OpenRouter to use AI Models, the old routes of TTS, LLM and STT will soon be removed.
The OpenRouter route called `chat` can receive audio inputs and soon will be able to receive images, the input looks like this:

**Content type:** `application/json`

``` json
{
  "contents": {
    "prompt": "What is being said in the music?",
    "audios": [
      {
        "format": "mp3",
        "data": "base64-formated-data"
      }
    ]
  },
  "model": "google/gemini-3.1-flash-lite"
}
```

**Notice:** The data in audios.data should be a valid base64 formated string, and the format should be a valid audio format.
**Notice:** The model must be compatible with audio input to procces audio and be an existing openrouter model.