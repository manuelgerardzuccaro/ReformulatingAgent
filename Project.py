import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    import requests
    from typing import Literal, Optional
    import argparse
    import sys

    # Ollama Configuration
    OLLAMA_URL = "http://localhost:11434/v1"
    MODEL_NAME = "codellama"

    # Supported style types
    Style = Literal["ironic", "empathetic", "professional", "poetic"]
    STYLES = ["ironic", "empathetic", "professional", "poetic"]

    return MODEL_NAME, OLLAMA_URL, STYLES, argparse, requests, sys


@app.cell
def _(MODEL_NAME, OLLAMA_URL, requests, sys):
    def rewrite_text(text: str, style: str, model: str = MODEL_NAME) -> str:
        """
        Send a request to the local model to rewrite the text according to the chosen style.
        """
        prompt = f"Rewrite the following text in {style} style:\n" + text

        payload = {
            "model": model,
            "prompt": prompt,
            "max_tokens": 512,
            "temperature": 0.7,
        }

        try:
            response = requests.post(f"{OLLAMA_URL}/completions", json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error calling Ollama: {e}", file=sys.stderr)
            sys.exit(1)

        data = response.json()
        return data.get("choices", [{}])[0].get("text", "")

    return (rewrite_text,)


@app.cell
def _(STYLES, argparse):
    def prompt_interactive() -> argparse.Namespace:
        text = input("Enter the text to rewrite: ")
        style = None
        while style not in STYLES:
            style = input(f"Choose the style ({', '.join(STYLES)}): ")
            if style not in STYLES:
                print(f"Invalid style, please try again.")
        return argparse.Namespace(text=text, style=style)
    return (prompt_interactive,)


@app.cell
def _(STYLES, argparse, prompt_interactive, rewrite_text):
    def main():
        parser = argparse.ArgumentParser(
            description="AI Agent for Creative Rewriting and Reframing"
        )
        parser.add_argument(
            "-t", "--text", help="Text to be rewritten"
        )
        parser.add_argument(
            "-s", "--style", choices=STYLES, help="Rewriting style"
        )
        args = parser.parse_args()

        # If args are missing, use interactive
        if not args.text or not args.style:
            print("Interactive mode: CLI arguments missing.")
            args = prompt_interactive()

        output = rewrite_text(args.text, args.style)
        print("\nRewritten text:\n")
        print(output)


    if __name__ == "__main__":
        main()

    return


if __name__ == "__main__":
    app.run()
