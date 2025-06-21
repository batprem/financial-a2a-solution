# financial-a2a-solution

# Run
## Prerequirement

`uv` command line from https://docs.astral.sh/uv/guides/scripts/

## Set up `.env`
Run
```
cp .env.example .env
```

Edit `.env` file by adding Gemini API key

## Start `Balance Sheet agent`

```
uv run balance-sheet-agent
```

## Start `technical-analyser-agent`

```
uv run technical-analyser-agent --port 9998
```

## Start main app

```
uv run tui
```