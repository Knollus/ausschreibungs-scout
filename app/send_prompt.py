"""
Rendert das Prompt-Template + Config und schickt es an OpenAI.
Erwartet: Umgebungsvariable OPENAI_API_KEY
"""

from pathlib import Path
import os, yaml, jinja2
from openai import OpenAI   # kommt aus "openai"-Paket

# ----- Pfade -------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent      # Projektwurzel
TEMPLATE = BASE / "templates" / "prompt_template.jinja"
CONFIG   = BASE / "config"    / "profile_dos.yml"

# ----- Prompt zusammenbauen ---------------------------------------------
def build_messages() -> list[dict]:
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE.parent),
        autoescape=False, trim_blocks=True, lstrip_blocks=True
    )
    rendered = env.get_template(TEMPLATE.name).render(**cfg)

    # Template enthält 2 Abschnitte – wir trennen sie an der Marker-Zeile
    system_marker = "{# ---------------- SYSTEM MESSAGE ---------------- #}"
    user_marker   = "{# ---------------- USER MESSAGE ---------------- #}"

    system_part, user_part = rendered.split(user_marker, 1)
    system_part = system_part.replace(system_marker, "").strip()
    user_part   = user_part.strip()

    return [
        {"role": "system", "content": system_part},
        {"role": "user",   "content": user_part},
    ]

# ----- API-Aufruf --------------------------------------------------------
def main():
    if "OPENAI_API_KEY" not in os.environ:
        raise RuntimeError(
            "OPENAI_API_KEY fehlt. Lege ihn als Codespaces-Secret oder "
            "als Terminal-Variable an."
        )

    client = OpenAI()    # Key wird automatisch aus ENV gelesen

    response = client.chat.completions.create(
        model="gpt-4o-mini",          # kostengünstig; bei Bedarf gpt-4o
        messages=build_messages(),
        temperature=0.1,
        max_tokens=2048,
    )

    print("\n--- Ergebnis ---\n")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
