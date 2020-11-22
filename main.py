from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import FileResponse

import mimetypes
import uvicorn
import hashlib
import shutil
import os
import magic

app = FastAPI()


@app.post("/upload")
async def image(file: bytes = File(...)):
    hash_object = hashlib.md5(file)
    file_hash = hash_object.hexdigest()

    save_dir = f"store/{file_hash[:2]}"
    print(save_dir, 'save path')
    os.makedirs(save_dir, exist_ok=True)
    save_path = save_dir + f'/{file_hash}'

    with open(save_path, "wb") as buffer:
        buffer.write(file)

    return {"hash": file_hash}


@app.get("/download")
async def main(file_hash: str):
    file_path = f'store/{file_hash[:2]}/{file_hash}'

    if os.path.exists(file_path):
        mimetype = magic.from_file(file_path, mime=True)
        return FileResponse(file_path, media_type=mimetype)
    else:
        return HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
