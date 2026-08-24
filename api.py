import os, sqlite3, hashlib, secrets
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from core import ingest_document, search_notes, get_document, list_sources

app = FastAPI(title="Personal Knowledge Base API")
DB = "users.db"

def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, password TEXT)")
    con.commit(); con.close()

def pw(x): return hashlib.sha256(x.encode()).hexdigest()
init_db()

@app.post("/signup")
def signup(username: str = Form(...), password: str = Form(...)):
    con = sqlite3.connect(DB)
    try:
        con.execute("INSERT INTO users VALUES (?,?)", (username, pw(password)))
        con.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(409, "User already exists")
    finally: con.close()
    return {"user_id": username}

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    con = sqlite3.connect(DB)
    row = con.execute("SELECT id FROM users WHERE id=? AND password=?", (username, pw(password))).fetchone()
    con.close()
    if not row: raise HTTPException(401, "Invalid credentials")
    return {"user_id": username}

@app.post("/upload")
async def upload(user_id: str = Form(...), file: UploadFile = File(...)):
    if Path(file.filename).suffix.lower() not in {".pdf",".md",".txt"}:
        raise HTTPException(400, "PDF/MD/TXT only")
    Path("uploads").mkdir(exist_ok=True)
    target = Path("uploads") / f"{secrets.token_hex(8)}_{Path(file.filename).name}"
    target.write_bytes(await file.read())
    return ingest_document(user_id, str(target))

@app.get("/search")
def search(user_id: str, q: str, top_k: int = 5):
    return search_notes(user_id, q, top_k)

@app.get("/sources")
def sources(user_id: str):
    return list_sources(user_id)

@app.get("/document/{doc_id}")
def document(doc_id: str, user_id: str):
    return get_document(user_id, doc_id)

@app.get("/", response_class=HTMLResponse)
def home():
    return Path("web/index.html").read_text(encoding="utf-8")
