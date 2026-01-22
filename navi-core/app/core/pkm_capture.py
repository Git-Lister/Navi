from pathlib import Path
import datetime
from app.models.pkm import CaptureRequest

# NaviG8 project root: ...\NaviG8\Navi\
NAVIG8_ROOT = Path(__file__).resolve().parents[3]
VAULT_ROOT = NAVIG8_ROOT / "Navi-vault"

def capture_to_markdown(req: CaptureRequest) -> Path:
    domain_dir = VAULT_ROOT / req.domain
    domain_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = (req.title or "note").replace(" ", "_")
    filename = f"{timestamp}_{slug}.md"
    path = domain_dir / filename

    frontmatter = [
        "---",
        f"domain: {req.domain}",
        f"title: {req.title or 'Untitled'}",
        f"source: {req.source or 'manual'}",
        f"created: {timestamp}",
        "status: raw",
        "---",
        "",
    ]
    body = req.content.strip() + "\n"
    path.write_text("\n".join(frontmatter) + body, encoding="utf-8")
    return path
