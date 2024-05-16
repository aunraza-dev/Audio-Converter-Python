from fastapi import FastAPI, File, UploadFile, Response
from pydub import AudioSegment
import os

app = FastAPI()

ALLOWED_EXTENSIONS = {'m4a', 'wma', 'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_mp3(input_file):
    audio = AudioSegment.from_file(input_file)
    mp3_file_path = os.path.splitext(input_file)[0] + ".mp3"
    audio.export(mp3_file_path, format="mp3")

    return mp3_file_path

@app.post("/convert/")
async def convert_file(file: UploadFile = File(...)):
    if not allowed_file(file.filename):
        return {"error": "Invalid file format. Allowed formats: m4a, wma, wav"}

    if not os.path.exists("temp"):
        os.makedirs("temp")

    input_file_path = f"temp/{file.filename}"
    with open(input_file_path, "wb") as buffer:
        buffer.write(await file.read())

    mp3_file_path = convert_to_mp3(input_file_path)

    os.remove(input_file_path)

    return {
        "message": "File converted successfully",
        "converted_file": mp3_file_path,
        "download_link": f"/download/{os.path.basename(mp3_file_path)}"
    }

@app.get("/download/{file_name}")
async def download_file(file_name: str, response: Response):
    file_path = f"temp/{file_name}"
    if os.path.exists(file_path):
        response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
        response.headers["Content-Type"] = "audio/mpeg"
        with open(file_path, "rb") as file:
            content = file.read()
        return Response(content, media_type="audio/mpeg")
    else:
        return {"error": "File not found"}
