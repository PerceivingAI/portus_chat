
# Portus_Chat

**Portus_Chat** is a privacy-conscious, API-compatible assistant that supports contextual conversation across OpenAI, Google Gemini, and xAI Grok models. Designed for CLI usage with SQLite-based local conversation storage, it offers both persistent and private modes.

## Features

- ✅ Full contextual memory
- 🧠 Support for OpenAI, Gemini, and Grok models
- 💾 Local SQLite storage of conversations
- 🔐 Private chat mode (no storage)
- 📜 CLI interface
- 🧰 Easily extensible provider architecture
- 🔄 `--reset-config` flag to restore default configuration
- 🧩 JSON-configured parameters for each provider

## Requirements

- Python 3.10+
- `openai`, `httpx`, `sqlite3`, `dotenv`, `tiktoken`

Install dependencies:

```bash
pip install -r requirements.txt
```

## .env Configuration

Before running the app, copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Then edit `.env` with your actual API keys:

```dotenv
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
GROK_API_KEY=your_grok_key_here
```

You only need to provide the key(s) for the provider(s) you plan to use. The app will load them automatically based on your selected provider in the config.

## Usage

Run the app:

```bash
python main.py
```

Run with reset:

```bash
python main.py --reset-config
```

## Configuration

The app uses a `portus_chat_config.json` at the root directory, which defines model URLs, keys, and behavior flags. This file is automatically created/reset with `--reset-config`.

## License

[MIT](LICENSE)

---

**Portus_Chat** is part of the Portus project family by [PerceivingAI](https://github.com/PerceivingAI).

Follow me on X https://x.com/PerceivingAI