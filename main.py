from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import csv
import io
import os

app = FastAPI()

# ✅ Enable CORS properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_TOKEN = "ean3tho9pdx7wnht"
MAX_SIZE = 83 * 1024  # 83 KB
ALLOWED_EXTENSIONS = {".csv", ".json", ".txt"}


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_9704: str = Header(None, alias="X-Upload-Token-9704"),
):
    # 1️⃣ Auth check
    if not x_upload_token_9704 or x_upload_token_9704 != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 2️⃣ File extension check
    filename = file.filename or ""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Bad Request")

    # 3️⃣ Read ONLY up to MAX_SIZE + 1 bytes
    contents = await file.read(MAX_SIZE + 1)

    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="Payload Too Large")

    # 4️⃣ CSV Processing
    if ext == ".csv":
        try:
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

            total_value = round(total_value, 2)

            return JSONResponse(content={
                "email": "23f2001645@ds.study.iitm.ac.in",
                "filename": filename,
                "rows": len(rows),
                "columns": columns,
                "totalValue": total_value,
                "categoryCounts": category_counts,
            })
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid CSV format")

    # 5️⃣ Non-CSV files
    return JSONResponse(content={
        "email": "23f2001645@ds.study.iitm.ac.in",
        "filename": filename,
        "message": "File accepted",
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5055,
        reload=True
    )
