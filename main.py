from fastapi import FastAPI, File, UploadFile, HTTPException
import mimetypes, os, shutil

app = FastAPI()

script_dir = os.path.dirname(os.path.abspath(__file__))
upload_folder = os.path.join(script_dir, "uploads")

os.makedirs(upload_folder, exist_ok=True)

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