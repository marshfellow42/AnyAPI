from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
from fastapi.responses import FileResponse
import mimetypes, os, shutil, sqlite3, json

with open("tags_metadata.json", "r") as file:
    tags_metadata = json.load(file)

app = FastAPI(openapi_tags=tags_metadata)

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
    return("API connected")

@app.post("/convert/pdf-to-png", tags=["Convert"])
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")

    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    script_path = os.path.join("tools", "convert", "pdf-to-png.py")

    os.system(f"python {script_path} {file_path}")

    return {"filename": file.filename, "message": "File uploaded and saved successfully", "path": file_path}

@app.get("/download/pdf-to-png/{filename}", tags=["Download"])
async def download_file(filename: str):
    download_folder = os.path.join(script_dir, "tools", "convert", "modified", "pdf-to-png")
    file_path = os.path.join(download_folder, filename)

    print(file_path)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=filename, media_type="application/zip")