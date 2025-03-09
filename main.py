from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
import mimetypes, os, shutil, sqlite3

app = FastAPI()

script_dir = os.path.dirname(os.path.abspath(__file__))
upload_folder = os.path.join(script_dir, "uploads")
db_path = os.path.join(script_dir, 'database.db')

os.makedirs(upload_folder, exist_ok=True)

if not os.path.exists(db_path):
   Path(db_path).touch()

with sqlite3.connect(db_path) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS TABLE (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            );
        ''')

@app.get("/")
def root():
    return("Hello World")

@app.post("/convert/pdf-to-png")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")

    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    os.system(f"python tools\\convert\\pdf-to-png.py {file_path}")

    return {"filename": file.filename, "message": "File uploaded and saved successfully", "path": file_path}
