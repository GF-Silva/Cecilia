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
