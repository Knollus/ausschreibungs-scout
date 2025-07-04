from pathlib import Path
import yaml, jinja2

BASE = Path(__file__).resolve().parent.parent
cfg_file = BASE / "config" / "profile_dos.yml"
template_dir = BASE / "templates"

# 1) Konfigurationsdaten laden
cfg = yaml.safe_load(cfg_file.read_text(encoding="utf-8"))

# 2) Template laden & rendern
env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                         autoescape=False, trim_blocks=True, lstrip_blocks=True)
prompt_raw = env.get_template("prompt_template.jinja").render(**cfg)

print(prompt_raw)
