import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
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
def _(STYLES, rewrite_text):
    def show_menu():
        print("\n=== Main Menu ===")
        print("1) Add a new style")
        print("2) Rewrite the text")
        print("3) Quit")
        choice = input("Select an option (1-3): ")
        return choice.strip()


    def add_style():
        new_style = input("Enter the name of the new style: ").strip()
        if not new_style:
            print("Invalid style name.")
        elif new_style in STYLES:
            print(f"The '{new_style}' style already exists.")
        else:
            STYLES.append(new_style)
            print(f"'{new_style}' style added.")


    def interactive_rewrite():
        text = input("\nEnter the text to rewrite: ")
        print("Available styles: " + ", ".join(STYLES))
        style = None
        while style not in STYLES:
            style = input("Choose the style to apply: ").strip()
            if style not in STYLES:
                print("Invalid style, please try again.")
        output = rewrite_text(text, style)
        print("\nRewritten text:\n")
        print(output)
    return add_style, interactive_rewrite, show_menu


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
    return


@app.cell
def _(add_style, interactive_rewrite, show_menu):
    def main():
        while True:
            choice = show_menu()
            if choice == '1':
                add_style()
            elif choice == '2':
                interactive_rewrite()
            elif choice == '3':
                print("Exit. Goodbye!")
                break
            else:
                print("Invalid choice, try again.")


    if __name__ == "__main__":
        main()

    return


if __name__ == "__main__":
    app.run()
