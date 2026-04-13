# Audiobook Summary Browser

A modern web-based browser for your audiobook summaries.

## Features
- Grid view of all 3,800+ book covers.
- Search by title or author.
- Integrated audio player (supports .opus).
- Markdown transcript viewer.
- Dark theme inspired by Audible.

## Setup & Run

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Run the Server**:
   ```bash
   cd audiobook_browser
   python3 server.py
   ```

3. **Access the Browser**:
   Open [http://localhost:8000](http://localhost:8000) in your web browser.

## Data Locations
- **Audio**: `/home/prime/Desktop/shared/Audiobooks`
- **Images**: `/home/prime/Desktop/devel/new_project/Personal_projects/youtube/Audiobooks/images`
- **Transcripts**: `/home/prime/Desktop/devel/new_project/Personal_projects/youtube/Audiobooks/transcripts`
- **Metadata**: `/home/prime/Desktop/devel/new_project/Personal_projects/youtube/Audiobooks/metadata.csv`
