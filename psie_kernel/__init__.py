"""PSIE Genesis Kernel v4 — Gând de Structurare ^ ∞. L0-L476 ACTIVE."""

import math
from collections import Counter

__version__ = "4.0.0"
__all__ = ["sdi_gate", "SDIVerdict", "CFC_MAX"]

CFC_MAX = 0.15
PRAG_SD = 0.80


class SDIVerdict:
    def __init__(self, sdi, cfc, ciclu, aprobat):
        self.sdi = sdi
        self.cfc = cfc
        self.ciclu = ciclu
        self.aprobat = aprobat

    def __repr__(self):
        return f"SDIVerdict(sdi={self.sdi:.4f}, cfc={self.cfc:.2f}, aprobat={self.aprobat})"


def _distributie(cuvinte):
    n = len(cuvinte)
    if n == 0:
        return {}
    c = Counter(cuvinte)
    return {w: v / n for w, v in c.items()}


def _entropie(dist):
    return -sum(p * math.log2(p) for p in dist.values() if p > 0)


def _informatie_partajata(dist_a, dist_b):
    """Informatia comuna celor doua distributii: suma min(pa,pb)·(-log2 min(pa,pb))."""
    mi = 0.0
    for w in set(dist_a) & set(dist_b):
        p = min(dist_a[w], dist_b[w])
        if p > 0:
            mi += p * -math.log2(p)
    return mi


def sdi_gate(original, imbunatatire, ciclu=1):
    """Verdict determinist: cat din imbunatatire e ancorat in substrat."""
    a = _distributie(str(original).lower().split())
    b = _distributie(str(imbunatatire).lower().split())
    h_b = _entropie(b) or 1e-9
    mi = _informatie_partajata(a, b)
    cfc = min(ciclu * 0.05, CFC_MAX)
    sdi = 1.0 - (mi / h_b) + cfc
    return SDIVerdict(round(sdi, 4), cfc, ciclu, sdi < PRAG_SD)
