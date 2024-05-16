Python script to convert m4a, wma, wav files to mp3.

Usage:

Run fastAPI application **uvicorn convert:app --reload** and visit **localhost:8000** and upload files you want converted
converted mp3s should be there when done.

REQUIRES:
ffmpeg (https://ffmpeg.org/download.html)
pydub pip install pydub

Tested to work with multiple formats. In theory it should also work with any other file type pydub allows.
