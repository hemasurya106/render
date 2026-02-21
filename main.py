from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import csv
import io
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_TOKEN = "ean3tho9pdx7wnht"
MAX_SIZE = 83 * 1024
ALLOWED_EXTENSIONS = {".csv", ".json", ".txt"}

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_9704: str = Header(None, alias="X-Upload-Token-9704"),
):
    if not x_upload_token_9704 or x_upload_token_9704 != VALID_TOKEN:
        raise HTTPException(status_code=401)

    filename = file.filename or ""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400)

    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=413)

    if ext == ".csv":
        text = contents.decode("utf-8")
        reader = csv.DictReader(io.StringIO(text))
        rows = list(reader)
        columns = list(rows[0].keys()) if rows else []

        total_value = 0.0
        category_counts = {}

        for row in rows:
            total_value += float(row["value"])
            cat = row["category"]
            category_counts[cat] = category_counts.get(cat, 0) + 1

        return JSONResponse(content={
            "email": "23f2001645@ds.study.iitm.ac.in",
            "filename": filename,
            "rows": len(rows),
            "columns": columns,
            "totalValue": round(total_value, 2),
            "categoryCounts": category_counts,
        })

    return {
        "email": "23f2001645@ds.study.iitm.ac.in",
        "filename": filename,
        "message": "File accepted",
    }
