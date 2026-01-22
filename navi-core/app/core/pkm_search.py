from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
from sentence_transformers import SentenceTransformer

NAVIG8_ROOT = Path(__file__).resolve().parents[3]
VAULT_ROOT = NAVIG8_ROOT / "Navi-vault"
INDEX_ROOT = VAULT_ROOT / ".navi_index"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class PKMSearchIndex:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)
        self.embeddings: np.ndarray | None = None
        self.docs: List[Dict[str, Any]] = []

    def _iter_notes(self) -> List[Path]:
        return list(VAULT_ROOT.rglob("*.md"))

    def build_index(self) -> None:
        INDEX_ROOT.mkdir(parents=True, exist_ok=True)
        notes = self._iter_notes()
        texts = []
        meta = []

        for p in notes:
            # Skip index dir itself
            if ".navi_index" in p.parts:
                continue
            text = p.read_text(encoding="utf-8")
            texts.append(text)
            meta.append({"path": str(p.relative_to(VAULT_ROOT))})

        if not texts:
            self.embeddings = None
            self.docs = []
            return

        vecs = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        self.embeddings = vecs
        self.docs = meta

        # Persist to disk
        np.save(INDEX_ROOT / "embeddings.npy", vecs)
        (INDEX_ROOT / "docs.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    def load_index(self) -> None:
        emb_path = INDEX_ROOT / "embeddings.npy"
        docs_path = INDEX_ROOT / "docs.json"
        if not emb_path.exists() or not docs_path.exists():
            self.embeddings = None
            self.docs = []
            return
        self.embeddings = np.load(emb_path)
        self.docs = json.loads(docs_path.read_text(encoding="utf-8"))

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        if self.embeddings is None or not len(self.docs):
            return []

        q_vec = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
        scores = np.dot(self.embeddings, q_vec)
        top_idx = np.argsort(-scores)[:k]

        results = []
        for i in top_idx:
            doc = self.docs[int(i)].copy()
            doc["score"] = float(scores[int(i)])
            results.append(doc)
        return results
