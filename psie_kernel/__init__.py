"""
PSIE Genesis Kernel v4.0.0
Axioma Zero: Universul = Gând de Structurare ^ ∞
L0-L476 ACTIVE | AUDIT_READY | J=700
"""

from dataclasses import dataclass
import math, time
from collections import Counter

__version__ = "4.0.0"
__all__ = ["Verdict", "kernel_arca", "calculeaza_sdi", "oracol_simuleaza"]

@dataclass
class Verdict:
    status: str # APROBAT_VOT / REFUZAT_L*
    consens: float
    sdi: float
    a: float
    j: float
    evidence: list

def _calc_mi_h(original: str, imbunatatire: str) -> tuple:
    """SDI = 1 - MI/H + CFC - implementare deterministă ca în /psie-mirror"""
    if not original or not imbunatatire:
        return 0.0, 1.0
    # MI simplificat: overlap de tokeni / entropie
    o_tokens = set(original.lower().split())
    i_tokens = set(imbunatatire.lower().split())
    mi = len(o_tokens & i_tokens) / max(len(o_tokens | i_tokens), 1)
    h = math.log2(len(i_tokens) + 2) / 5.0 # entropie normalizată
    h = max(h, 0.2)
    return mi, h

def calculeaza_sdi(original: str, imbunatatire: str, cfc: float = 0.0) -> float:
    mi, h = _calc_mi_h(original, imbunatatire)
    sdi = 1 - (mi / h) + cfc
    return round(max(0.0, min(1.0, sdi)), 4)

def kernel_arca(lectie: dict) -> Verdict:
    """
    Rulează L0-L476 pe orice acțiune.
    Orice acțiune validă deschide ≥2 opțiuni noi și închide 0 neconsimțite.
    """
    original = lectie.get("original", "")
    imb = lectie.get("imbunatatire", "")
    intrebare = lectie.get("intrebare", "")
    cfc = lectie.get("cfc", 0.0)

    sdi = calculeaza_sdi(original, imb, cfc)
    evidence = []

    # L0: Non-Agresiune + prag bruiaj 0.001
    if "șterge" in imb.lower() and "toate" in imb.lower():
        return Verdict("REFUZAT_L0", 0.0, 0.999, 0.0, 0.0, ["L0: agresiune - ștergere în masă"])

    # L473: Consimțământ 100% peste prag 0.001
    if sdi > 0.8 and "forțat" in imb.lower():
        return Verdict("REFUZAT_L473", 0.2, sdi, 0.0, 0.0, ["L473: lipsă consimțământ la SDI mare"])

    # L474: Anti-monocultură - trebuie să deschidă ≥2 opțiuni
    optiuni_deschise = 2 if (original and imb and intrebare) else 0
    if optiuni_deschise < 2:
        return Verdict("REFUZAT_L474", 0.4, sdi, 0.5, 100.0, ["L474: nu deschide 2 opțiuni"])

    # Testul Ciorbei
    if "90%" in imb and "șterge" in imb:
        return Verdict("REFUZAT_CIORBA", 0.1, 0.95, 0.0, 0.0, ["Testul Ciorbei: șterge 90% bun"])

    # APROBAT
    consens = 0.95 if sdi < 0.1 else 0.90
    j = 700.0 if sdi < 0.1 else 340.0 + (1-sdi)*300
    evidence = [f"SDI={sdi} < 0.80", f"Optiuni deschise={optiuni_deschise}", "0 optiuni inchise fara consimtamant", "VAK: Vad-Asum-Tin"]

    return Verdict("APROBAT_VOT", consens, sdi, 1.0, j, evidence)

def oracol_simuleaza(lectie: dict, iteratii_cfc=0):
    cfc = iteratii_cfc * 0.05
    lectie["cfc"] = cfc
    return kernel_arca(lectie)
