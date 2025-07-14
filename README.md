# ReformulatingAgent

An AI agent for creative rewriting and reframing of text (emails, essays, tweets, etc.) in different styles (ironic, empathetic, professional, poetic).

---

## Features

- **Multi‑style rewriting**: choose from "ironic", "empathetic", "professional", "poetic".
- **Interactive CLI**: enter text and select a style in the terminal, or pass arguments via command line.
- **Powered by Ollama**: leverages a local model (e.g. `codellama`) running on Ollama.
- **Easily extensible**: add new styles or models by updating just a few lines of code.

---

## Prerequisites

- Python ≥ 3.10  
- [Ollama](https://ollama.ai/) running locally (default `http://localhost:11434`)  
- A compatible model installed in Ollama (e.g. `codellama`)  
- Python dependencies (installable via `poetry`)

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/manuelgerardzuccaro/ReformulatingAgent.git
   cd ReformulatingAgent
2. **Install dependencies**  
   ```bash
   # Using Poetry
   poetry install

## Configuration
To change the Ollama endpoint or default model, edit the constants in Project.py:
```py
OLLAMA_URL = "http://localhost:11434/v1"
MODEL_NAME = "codellama"
```
## Usage
### Non‑interactive mode
Pass text and style directly:
```bash
python Project.py -t "The meeting has been postponed until tomorrow." -s ironic
```
### Interactive mode
Run without arguments to be guided step‑by‑step:
```bash
python Project.py
# Enter your text…
# Choose a style (ironic, empathetic, professional, poetic):
```

## Project Structure
```bash
ReformulatingAgent/
├── Project.py         # Main application (script + CLI)
├── pyproject.toml     # Package configuration
├── README.md
└── .gitignore

```






