# llm-learning

Study project for building a function-calling coding agent with Gemini.

This repository demonstrates how an LLM can:

- receive a user prompt,
- decide to call local tools,
- execute safe file operations in a restricted directory,
- and return a final response.

The project includes a small sandbox app (`calculator/`) that the agent can inspect, run, and modify through tool calls.

## Language Versions

- English: this file (`README.md`)
- Portuguese (Brazil): `README.pt-BR.md`

## What This Project Does

At runtime, `main.py` sends your prompt to Gemini with:

- a system prompt (`promps.py`),
- a set of tool/function declarations (`call_function.py`),
- and the conversation history.

Gemini can request one or more function calls. Each function call is executed locally, the result is sent back to Gemini, and the loop continues until Gemini returns a final text answer (or max iterations is reached).

The four tools exposed to the model are:

1. `get_files_info`: list files in a directory.
2. `get_file_content`: read text file content.
3. `write_file`: create/overwrite files.
4. `run_python_file`: execute a Python script.

## Security Model

All tool paths are constrained to a working directory (`./calculator`) injected in `call_function.py`.

Path validation is centralized in `functions/path_validation.py`:

- paths are normalized with `os.path.abspath(os.path.join(...))`,
- `os.path.commonpath` verifies target is inside the allowed root,
- access outside root (for example `../` or `/bin`) is blocked.

This is the key safety mechanism that prevents directory traversal and accidental access to arbitrary filesystem locations.

## Repository Structure

### Root

- `main.py`: CLI app and agent loop.
- `call_function.py`: function registry and dispatcher.
- `promps.py`: system prompt used by Gemini.
- `config.py`: constants (`MAX_CHARACTERS`).
- `pyproject.toml`: Python project metadata and dependencies.
- `test_*.py`: manual test scripts for each tool.

### tools (`functions/`)

- `functions/path_validation.py`: reusable path safety guard.
- `functions/get_files_info.py`: directory listing with size and dir flag.
- `functions/get_file_content.py`: reads file content with truncation marker behavior.
- `functions/write_file.py`: writes text files, creates parent directories.
- `functions/run_python_file.py`: runs `.py` files via subprocess and returns stdout/stderr.

### sandbox app (`calculator/`)

- `calculator/main.py`: simple calculator CLI.
- `calculator/pkg/calculator.py`: infix expression evaluator (`+ - * /`, precedence, parentheses).
- `calculator/pkg/render.py`: renders JSON output.
- `calculator/tests.py`: unit tests for calculator behavior.
- `calculator/lorem.txt`, `calculator/pkg/morelorem.txt`: sample writable files.

## Installation

### 1. Requirements

- Python 3.13+
- A Gemini API key

### 2. Install dependencies

Using `uv`:

```bash
uv sync
```

Or with `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install google-genai==1.12.1 python-dotenv==1.1.0
```

### 3. Configure environment variables

Create `.env` in project root:

```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

Basic usage:

```bash
python main.py "List files in the current directory"
```

Verbose mode:

```bash
python main.py --verbose "Read main.py and explain it"
```

### What happens when you run it

1. CLI parses your prompt.
2. Message is sent to Gemini with tool definitions.
3. Gemini may request tool calls.
4. Local tool executes in `./calculator` scope.
5. Tool result is appended to conversation.
6. Loop repeats until final model answer.

## Testing

Run the tool test scripts:

```bash
python test_get_files_info.py
python test_get_file_content.py
python test_write_file.py
python test_run_python_file.py
```

### Current observed behavior

Tool tests validate that blocked paths like `/bin`, `../`, and `/tmp/temp.txt` are rejected.

`test_run_python_file.py` currently reveals one calculator unit test failure (`test_not_enough_operands`) because expression `"+ 3"` raises `IndexError` instead of the expected `ValueError`.

## Notes and Limitations

- `get_file_content` currently reads the first 1000 characters, while truncation text mentions `MAX_CHARACTERS` (10000). This mismatch is useful to fix in a future refactor.
- In tool modules, exception handlers use `return print(...)`, which returns `None` after printing. Returning explicit error strings would simplify upstream handling.
- File `promps.py` contains a typo in filename (`promps` vs `prompts`) but works as imported.

## Learning Goals Covered

This repo is a good minimal reference for:

- function-calling LLM workflows,
- secure filesystem tooling,
- subprocess execution with constrained scope,
- iterative tool-call loops with conversation state,
- and test-driven exploration of edge cases.
