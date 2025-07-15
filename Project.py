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
    import json
    from pathlib import Path

    # File where to store styles (name -> description)
    STYLES_FILE = Path("styles.json")

    # Ollama Configuration
    OLLAMA_URL = "http://localhost:11434/v1"
    MODEL_NAME = "codellama"
    return MODEL_NAME, OLLAMA_URL, STYLES_FILE, argparse, json, requests, sys


@app.cell
def _(STYLES_FILE, json, sys):
    def load_styles() -> dict[str, str]:
        """
        Load styles from a JSON file. Returns a dict mapping style names to descriptions.
        """
        if STYLES_FILE.exists():
            try:
                with STYLES_FILE.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                # only accept a dict of str->str
                if isinstance(data, dict) and all(isinstance(k, str) and 
                                                  isinstance(v, str) for k,v in data.items()):
                    return data
                else:
                    print("Warning: styles.json has invalid format, using default styles.", 
                          file=sys.stderr)
            except json.JSONDecodeError:
                print("Warning: styles.json corrupt, using default styles.", 
                      file=sys.stderr)

        # Default styles if file missing or corrupted
        return {
            "ironic": "Strong sense of irony and sarcasm.",
            "empathetic": "Empathy and understanding, showing compassion.",
            "professional": "Clear, formal, and professional tone.",
            "poetic": "Lyrical, poetic language and vivid tones."
        }

    def save_styles(styles: dict[str, str]) -> None:
        """
        Save the styles mapping to a JSON file.
        """
        with STYLES_FILE.open("w", encoding="utf-8") as f:
            json.dump(styles, f, ensure_ascii=False, indent=2)

    # Load style definitions
    STYLES: dict[str, str] = load_styles()
    return STYLES, save_styles


@app.cell
def _(MODEL_NAME, OLLAMA_URL, requests, sys):
    def rewrite_text(text: str, style_name: str, style_desc: str, model: str = MODEL_NAME) -> str:
        """
        Send a request to the local model to rewrite the text according to the chosen style.
        """
        prompt = f"Rewrite the following text in {style_name} style ({style_desc}):\n" + text

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
def _(STYLES: dict[str, str], STYLES_FILE, rewrite_text, save_styles):
    def show_menu():
        print("\n=== Main Menu ===")
        print("1) Rewrite the text")
        print("2) Add a new style")
        print("3) Quit")
        choice = input("Select an option (1-3): ")
        return choice.strip()


    def add_style():
        """
        Prompt the user to add a new style with a description.
        """
        name = input("Enter the name of the new style: ").strip()
        if not name:
            print("Invalid style name.")
            return
        if name in STYLES:
            print(f"The '{name}' style already exists.")
            return
        desc = input("Enter a description for how this style should rewrite text: ").strip()
        if not desc:
            print("Description cannot be empty.")
            return
        STYLES[name] = desc
        save_styles(STYLES)
        print(f"'{name}' style added with description and saved to {STYLES_FILE}.")


    def interactive_rewrite():
        """
        Prompt the user for text and style, then display the rewritten text.
        """
        text = input("\nEnter the text to rewrite: ")
        print("Available styles:")
    
        for style, desc in STYLES.items():
            print(f"- {style}: {desc}")

        choice = None
    
        while choice not in STYLES:
            choice = input("Choose the style name to apply: ").strip()
            if choice not in STYLES:
                print("Invalid style, please try again.")

        # Pass both the style name and its description
        output = rewrite_text(text, choice, STYLES[choice])
        print("\nRewritten text:\n")
        print(output)
    return add_style, interactive_rewrite, show_menu


@app.cell
def _(STYLES: dict[str, str], argparse):
    def prompt_interactive() -> argparse.Namespace:
        """
        Prompt for CLI usage: returns namespace with text and style.
        """
        text = input("Enter the text to rewrite: ")
        print("Choose a style:")
        for s in STYLES:
            print(f"- {s}")
        style = None
        while style not in STYLES:
            style = input(f"Choose the style ({', '.join(STYLES.keys())}): ")
            if style not in STYLES:
                print("Invalid style, please try again.")
        return argparse.Namespace(text=text, style=style)
    return


@app.cell
def _(add_style, interactive_rewrite, show_menu):
    def main():
        while True:
            choice = show_menu()
            if choice == '1':
                interactive_rewrite()
            elif choice == '2':
                add_style()
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
