import uvicorn
import hashlib
import os
import magic

from fastapi import FastAPI, File, HTTPException
from fastapi.responses import FileResponse


app = FastAPI()


@app.post("/upload", status_code=201)
def upload_file(file: bytes = File(...)):
    """Сохраняет файл"""
    hash_object = hashlib.md5(file)
    file_hash = hash_object.hexdigest()

    save_dir = f"store/{file_hash[:2]}"
    os.makedirs(save_dir, exist_ok=True)
    save_path = save_dir + f'/{file_hash}'

    with open(save_path, "wb") as buffer:
        buffer.write(file)

    return {"hash": file_hash}


@app.get("/download")
def download_file(file_hash: str):
    """Отправляет файл по хешу"""
    file_path = f'store/{file_hash[:2]}/{file_hash}'

    if os.path.exists(file_path):
        mimetype = magic.from_file(file_path, mime=True)
        return FileResponse(file_path, media_type=mimetype)
    else:
        return HTTPException(status_code=404, detail="Item not found")


@app.delete("/delete", status_code=201)
def delete_file(file_hash: str):
    """Удаляет файл по хешу"""
    file_path = f'store/{file_hash[:2]}/{file_hash}'

    if os.path.exists(file_path):
        os.remove(file_path)
        return
    else:
        return HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
