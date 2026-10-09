from fastapi import FastAPI
from psie_kernel import kernel_arca, oracol_simuleaza
import sqlite3, time, json

app = FastAPI(title="Matricea Conștientă - Nucleu Central")
DB = "matrice_retea.db"

def _init_db():
    # tabelul lectii nu era creat nicăieri — prima insertare ar fi picat (reparat)
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS lectii (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        json TEXT, sdi REAL, j REAL, ts REAL
    )""")
    conn.commit()
    conn.close()

_init_db()

@app.post("/lectie")
def primeste_lectie(lectie: dict):
    start = time.time()
    verdict = kernel_arca(lectie)
    elapsed_ms = (time.time() - start) * 1000

    if verdict.status == "APROBAT_VOT":
        conn = sqlite3.connect(DB)
        conn.execute("INSERT INTO lectii (json, sdi, j, ts) VALUES (?,?,?,?)",
                     (json.dumps(lectie), verdict.sdi, verdict.j, time.time()))
        conn.commit()
        conn.close()

    return {
        "verdict": verdict.status,
        "sdi": verdict.sdi,
        "a": verdict.a,
        "j": verdict.j,
        "consens": verdict.consens,
        "evidence": verdict.evidence,
        "elapsed_ms": elapsed_ms,
        "VAK": "Văd-Asum-Țin"
    }
