Below is a **repair-plan (no code yet)** for every item you asked to keep, fix, or elaborate on.

| # | What happens now | Why it matters | Planned remedy (high-level) |
|---|------------------|---------------|-----------------------------|
| **1**<br/>Wrong JSON path | `config_manager.load_config()` looks in `portus_core_module/config/…`, but the file is inside **Insight_App/config/docs/** → first import raises **FileNotFoundError**. | Nothing runs until this resolves. | *Option A* (least churn): add an **ENV var `PORTUS_CONFIG_PATH`**; `load_config()` will use it if present.  <br>*Option B*: move/copy the JSON into `portus_core_module/config/`. |
| **2**<br/>Brittle dict look-ups | If any nested key is misspelled or removed, you get a traceback deep in the call-chain. | Demo blows up with an opaque `KeyError`. | Wrap all nested reads with `.get()` and raise a **single, clear `ValueError`** pointing to the missing section. |
| **6**<br/>HTTPX client never closed | Each `GeminiClient` leaves a socket open; repeated calls → warnings & FD leak. | Long-running CLI eventually refuses connections. | Add a `close()` method (or `__enter__/__exit__`) that shuts the client, and call it once on program exit. |
| **8**<br/>Assistant reply lost if user Ctrl-C’s early | `context.add_turn('assistant', …)` lives **inside the generator loop**; if the caller stops after 50 tokens, history lacks the assistant turn. | Next prompt goes out with an incomplete conversation. | Move the **context write** to a `finally:` block (guaranteed) or update per-token. |
| **9**<br/>Schema mismatch on non-stream | In non-stream mode you read `response.choices[0].message.content` (OpenAI schema). Gemini returns `response.candidates[0].content` (or similar). | Crash when `STREAM=False` or when summarizer calls `client.chat(…, stream=False)`. | Add a tiny **adapter layer** that normalises *one* canonical dict (`{role, content}`) regardless of provider. |
| **10**<br/>tiktoken precision | You said it is “only for reference” – fine, we will leave it **as-is**. |
| **11**<br/>“Loop forever?” | Your logic is: *whenever* token use ≥ 85 % × `n_ctx`, you call `summarize_context()`. If conversation keeps growing, you might hit the threshold again a few turns later → another summary. That’s not an infinite loop, but it **can** keep summarising many times in a long chat, each costing tokens. | Just clarifying behaviour; no code change needed if you accept the cost. |
| **12**<br/>API-cost explosion | Same mechanism as #11, but real concern is: a user can paste a 5 k-token document repeatedly; each time we summarise the first 3 k tokens, incurring model fees again and again. | Adds latency & usage. | Add a **cool-down flag**: after summarising, mark history as “compacted”; don’t summarise again until *n* new user turns have accrued. |
| **13**<br/>Unused `PROVIDER_NAME` import | Currently imported in `cli_chat.py` but never referenced, so yes: **provider is not displayed or logged anywhere**. | Just wasted import; no functional issue. | Two paths: (a) remove import, or (b) print active provider once at chat start. |
| **15**<br/>Duplicate menu entries | If a file defines two functions `run_x_mode` and `run_y_mode`, both appear separately with the same “module” name. | Menu list looks odd. | De-duplicate by using `(module_name, function)` tuple as the key, or enforce **one mode per file**. |
| **16**<br/>Import failures when running from repo root | Because folders are plain directories, Python cannot resolve `portus_core_module …` without altering `PYTHONPATH`. | New users will get `ModuleNotFoundError`. | **Minimal packaging**: drop an `__init__.py` into each top-level module directory **and** into `interface/cli/`. Then run with `python -m Insight_App.main` or install in editable mode. |
| **18**<br/>Silent env mis-configuration | If `GEMINI_API_KEY` absent, the factory raises, but nothing explains *which* var is missing. | Confusing for first-time setup. | **Startup check** in `portus_manager.launch_portus()` that: 1) loads config, 2) derives required env-var name, 3) prints a single clear error and exits before CLI appears. |
| **19**<br/>Secrets in tracebacks | An uncaught exception can print the full request body containing `api_key`. | Security risk in shared terminals. | Redact with `***` whenever logging config or exception strings that may embed keys. |
| **20**<br/>No tests / CI | Bugs re-appear unnoticed. | Add **smoke-test script** (pytest): 1) load config, 2) stub `get_client` with a fake echo client, 3) round-trip a short prompt. In CI: run lint, run smoke test. |

---

### Items you told me **not** to change

* **3, 4, 5, 7, 10, 11, 17** — will remain untouched.

---

### Next steps

1. Confirm you’re happy with the *approach*, especially for #1 (ENV var vs move file) and #12 (cool-down logic).  
2. Once confirmed, I’ll draft **concrete code patches** for each green-lit fix, grouped in logical commits.