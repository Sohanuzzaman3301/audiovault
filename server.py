import os
import csv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uvicorn

app = FastAPI()

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths to your data
AUDIO_DIR = Path("/home/prime/Desktop/shared/Audiobooks")
IMAGES_DIR = AUDIO_DIR / "images"
TRANSCRIPTS_DIR = AUDIO_DIR
METADATA_CSV = Path("/home/prime/Desktop/devel/new_project/Personal_projects/youtube/Audiobooks/metadata.csv")

# Serve static files
app.mount("/static/audio", StaticFiles(directory=str(AUDIO_DIR)), name="audio")
app.mount("/static/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")
app.mount("/static/transcripts", StaticFiles(directory=str(TRANSCRIPTS_DIR)), name="transcripts")

def load_metadata():
    books = []
    
    # 1. Try to load from CSV if it exists
    csv_data = {}
    if METADATA_CSV.exists():
        with open(METADATA_CSV, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filename = row.get("Filename", "")
                if filename:
                    csv_data[filename] = row

    # 2. Scan the audio directory for all .opus files
    for audio_file in AUDIO_DIR.glob("*.opus"):
        filename = audio_file.name
        stem = audio_file.stem
        
        # Determine title and author
        if filename in csv_data:
            title = csv_data[filename].get("Album", stem)
            author = csv_data[filename].get("Artist", "Unknown")
        else:
            # Fallback: Parse "Title (Author).opus"
            if "(" in stem and stem.endswith(")"):
                title = stem[:stem.rfind("(")].strip()
                author = stem[stem.rfind("(")+1:-1].strip()
            else:
                title = stem
                author = "Unknown"
        
        # Check for cover and transcript
        # Images are in IMAGES_DIR/{stem}.jpg
        cover_exists = (IMAGES_DIR / f"{stem}.jpg").exists()
        
        # Transcripts might be {stem}.opus.srt or {stem}.srt or {stem}.md
        transcript_file = None
        for ext in [".opus.srt", ".srt", ".md", ".txt"]:
            if (TRANSCRIPTS_DIR / (stem + ext)).exists():
                transcript_file = stem + ext
                break
        
        books.append({
            "id": stem,
            "title": title,
            "author": author,
            "filename": filename,
            "cover": f"/static/images/{stem}.jpg" if cover_exists else None,
            "audio": f"/static/audio/{filename}",
            "transcript": f"/static/transcripts/{transcript_file}" if transcript_file else None
        })
        
    return books

@app.get("/api/books")
async def get_books():
    try:
        return load_metadata()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def serve_index():
    from fastapi.responses import FileResponse
    return FileResponse("index.html")

if __name__ == "__main__":
    print(f"Starting server... Access at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
