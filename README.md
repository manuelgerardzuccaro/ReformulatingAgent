# ReformulatingAgent

A tool for rewriting text and managing custom styles using a local LLM server.

## Requirements

- **Python 3.10** or higher
  - Download and install from [python.org](https://www.python.org/downloads/)
- **Ollama** (local LLM server)

## Installation

### 1. Install and Start Ollama

1. Visit [https://ollama.com](https://ollama.com/download) and download the Windows installer.
2. Run the installer.

> After installation, Ollama is configured to start automatically in the background at system startup and will listen on `http://localhost:11434`.

3. If the service does not start automatically, run the following command in your terminal:

```bash
ollama serve
```

4. Download an LLM model (e.g., CodeLlama):

```bash
ollama pull codellama
```

5. List all downloaded models:

```bash
ollama list
```

### 2. Configure the Model

1. Open `config.json` in the project root.
2. Ensure the `MODEL_NAME` field matches the model you pulled (e.g., `codellama`).

```c
{
  "MODEL_NAME": "codellama",
   //... other settings ...
}
```

### 3. Install Project Dependencies

1. Install **Poetry** (Python dependency manager):

   ```bash
   pip install poetry
   ```

2. Clone the repository and navigate into it:

   ```bash
   git clone https://github.com/manuelgerardzuccaro/ReformulatingAgent.git
   cd ReformulatingAgent
   ```
     (or ssh-version: `git@github.com:manuelgerardzuccaro/ReformulatingAgent.git`)

3. Install the project's dependencies with Poetry:

   ```bash
   poetry install
   ```

4. Install **Marimo** (for reactive notebooks):

   ```bash
   pip install marimo
   ```

## Usage

### 1. Interactive Notebook (Marimo)

Launch the reactive notebook:

```bash
poetry run marimo edit Project.py
```

### 2. Command-Line Application

Run the application directly:

```bash
poetry run python Project.py
```

When the application starts, you will see a main menu with the following options:

1. **Rewrite the text**
2. **Add a style** (`<name, description>`)
3. **Quit**


## Project Structure

```bash
ReformulatingAgent/
├── Project.py         # Main application
├── config.json        # Settings (e.g., MODEL_NAME)
├── styles.json        # Style definitions: a map of <"style_name": "description">
├── pyproject.toml     # Poetry package and dependency config
├── README.md          # This documentation file
└── .gitignore         
```
---
