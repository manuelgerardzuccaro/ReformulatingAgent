import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    print ("")
    return


@app.cell
def _():
    import requests
    from typing import Literal, Optional
    import argparse
    import sys

    # Configurazione Ollama
    OLLAMA_URL = "http://localhost:11434/v1"
    MODEL_NAME = "codellama"

    # Tipi di stile supportati
    Style = Literal["ironico", "empatico", "professionale", "poetico"]
    STYLES = ["ironico", "empatico", "professionale", "poetico"]

    return MODEL_NAME, OLLAMA_URL, STYLES, argparse, requests, sys


@app.cell
def _(MODEL_NAME, OLLAMA_URL, requests, sys):
    def rewrite_text(text: str, style: str, model: str = MODEL_NAME) -> str:
        """
        Invia una richiesta al modello locale per riscrivere il testo secondo lo stile scelto.
        """
        prompt = f"Riscrivi il seguente testo in stile {style}:\n" + text

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
            print(f"Errore nella chiamata a Ollama: {e}", file=sys.stderr)
            sys.exit(1)

        data = response.json()
        return data.get("choices", [{}])[0].get("text", "")

    return (rewrite_text,)


@app.cell
def _(STYLES, argparse):
    def prompt_interactive() -> argparse.Namespace:
        text = input("Inserisci il testo da riscrivere: ")
        style = None
        while style not in STYLES:
            style = input(f"Scegli lo stile ({', '.join(STYLES)}): ")
            if style not in STYLES:
                print(f"Stile non valido, riprova.")
        return argparse.Namespace(text=text, style=style)
    return (prompt_interactive,)


@app.cell
def _(STYLES, argparse, prompt_interactive, rewrite_text):
    def main():
        parser = argparse.ArgumentParser(
            description="Agent AI per riscrittura creativa e reframing"
        )
        parser.add_argument(
            "-t", "--text", help="Testo da riscrivere"
        )
        parser.add_argument(
            "-s", "--style", choices=STYLES, help="Stile di riscrittura"
        )
        args = parser.parse_args()

        # Se mancano argomenti, usa interattivo
        if not args.text or not args.style:
            print("Modalità interattiva: mancano argomenti CLI.")
            args = prompt_interactive()

        output = rewrite_text(args.text, args.style)
        print("\nTesto riscritto:\n")
        print(output)


    if __name__ == "__main__":
        main()

    return


if __name__ == "__main__":
    app.run()
