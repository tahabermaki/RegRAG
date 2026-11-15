"""Télécharge le corpus de démo décrit dans corpus/manifest.yaml.

Usage : python scripts/download_corpus.py   (ou `make corpus`)

Pour chaque document : téléchargement dans data/raw/<id>.pdf, puis écriture d'un
fichier de verrouillage (URL, date, taille, SHA-256). C'est la base de la
traçabilité : on sait toujours de quelle version d'un texte vient une réponse.
"""

import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import httpx
import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "corpus" / "manifest.yaml"
OUT_DIR = ROOT / "data" / "raw"
LOCK = OUT_DIR / "manifest.lock.json"


def main() -> int:
    docs = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))["documents"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lock = json.loads(LOCK.read_text()) if LOCK.exists() else {}
    failures = 0

    with httpx.Client(follow_redirects=True, timeout=120, headers={"User-Agent": "regrag/0.1"}) as client:
        for doc in docs:
            if not doc.get("enabled") or not doc.get("url"):
                print(f"- {doc['id']:<22} ignoré (désactivé ou sans URL)")
                continue
            target = OUT_DIR / f"{doc['id']}.pdf"
            try:
                resp = client.get(doc["url"])
                resp.raise_for_status()
            except httpx.HTTPError as exc:
                print(f"x {doc['id']:<22} ÉCHEC : {exc}")
                failures += 1
                continue
            target.write_bytes(resp.content)
            sha = hashlib.sha256(resp.content).hexdigest()
            changed = lock.get(doc["id"], {}).get("sha256") not in (None, sha)
            lock[doc["id"]] = {
                "title": doc["title"],
                "url": doc["url"],
                "downloaded_at": datetime.now(UTC).isoformat(timespec="seconds"),
                "bytes": len(resp.content),
                "sha256": sha,
            }
            flag = "  (NOUVELLE VERSION)" if changed else ""
            print(f"✓ {doc['id']:<22} {len(resp.content) / 1e6:5.1f} Mo  {sha[:12]}{flag}")

    LOCK.write_text(json.dumps(lock, indent=2, ensure_ascii=False))
    print(f"\nVerrou écrit : {LOCK.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
