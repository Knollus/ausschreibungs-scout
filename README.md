# ausschreibungs-scout

Dieses Projekt sammelt aktuelle EU-Ausschreibungen (TED) und baut daraus
einen Prompt für die OpenAI API.

## Voraussetzungen

- Python 3.11 oder neuer
- Abhängigkeiten aus `requirements.txt`
- Eine Umgebungsvariable `OPENAI_API_KEY`

## Nutzung

1. Die Filter in `config/profile_dos.yml` anpassen.
2. Prompt lokal erzeugen:

   ```bash
   python app/build_prompt.py
   ```

3. Prompt an OpenAI schicken:

   ```bash
   OPENAI_API_KEY=<dein_schlüssel> python app/send_prompt.py
   ```
