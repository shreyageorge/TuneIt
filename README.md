# TuneIt — Digital Music Library Manager

A small Django + Python DSA project with a Spotify-inspired interface. The main screen is the music player; the **DSA Operations** screen demonstrates the required BST insertion/deletion/title search, binary search on a duration-sorted array, and merge sort by duration, including comparison counts.

## Open in VS Code
1. Extract the ZIP, open the **TuneIt** folder in VS Code.
2. Open a terminal in that folder. Python 3.10+ and pip are required.
3. Create a virtual environment: `python -m venv .venv`
4. Activate it on Windows PowerShell: `.venv\Scripts\Activate.ps1` (or use `.venv\Scripts\python.exe` directly).
5. Install Django: `pip install "Django>=5.2,<6"`
6. Start quickly using SQLite: `python manage.py migrate --run-syncdb`
7. Seed 27 songs with YouTube video links: `python manage.py shell -c "from music.seed import seed; seed()"`
8. Run: `python manage.py runserver`
9. Open http://127.0.0.1:8000/ in your browser.

## Deploy to Vercel
1. Import `https://github.com/shreyageorge/TuneIt` into Vercel and set the project root to the repository root (the folder containing `manage.py`).
2. Before deploying, add these environment variables in **Project Settings → Environment Variables** for Production (and Preview if desired): `DJANGO_SECRET_KEY` (generate one locally with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`), `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, and `MYSQL_PORT`. Never commit these values. `DJANGO_DEBUG` should be unset or set to `0`. If using a custom domain, add it to `DJANGO_ALLOWED_HOSTS` as a comma-separated host list.
3. Deploy. Vercel runs `collectstatic` during the build and serves the Django WSGI application from `api/index.py`; WhiteNoise serves the collected static files.
4. Initialize the hosted MySQL database once from a terminal with the same `MYSQL_*` variables set: run `python manage.py migrate --run-syncdb`, then `python manage.py shell -c "from music.seed import seed; seed()"`. Ensure the database host accepts connections from Vercel and configure any provider-required TLS settings.

Vercel's function filesystem is not persistent, so do not use the default SQLite database for a deployed app. Use a hosted MySQL instance for song and playlist data. Vercel does not run Django migrations automatically; run the initialization commands above whenever deploying schema changes.

## Switch to MySQL
Install MySQL Server, create a database named `tuneit`, then install the packages from `requirements.txt`. The project uses PyMySQL as its pure-Python MySQL driver, avoiding a native extension build. Set environment variables `MYSQL_DATABASE=tuneit`, `MYSQL_USER`, `MYSQL_PASSWORD`, and optionally `MYSQL_HOST`, `MYSQL_PORT`. Run `python manage.py migrate --run-syncdb` and the seed command again. Django selects MySQL whenever `MYSQL_DATABASE` is set. SQLite is provided only to make initial testing easier.

## What is stored where?
- `Song`: one record per song (title unique, artist, duration in seconds, optional playable audio/YouTube and cover URLs).
- `Playlist`: one record per playlist.
- `PlaylistSong`: references song IDs and playlist IDs; no repeated song metadata.
- `music/dsa.py`: manually implemented BST, merge sort and binary search. Algorithm nodes and temporary sorting arrays hold song IDs only; title and duration comparisons read those fields from the database. The BST and merge-sort workspaces are rebuilt for each operation.

## Important notes
- The seeded catalog uses real song titles and artists and links to YouTube official music videos. Clicking a song with a YouTube link opens YouTube's embedded player inside TuneIt; videos that disallow embedding may not play there.
- When adding a song, enter a direct browser-playable audio URL or a YouTube video URL in the Audio or YouTube URL field. YouTube links are played using YouTube's embedded player, not as MP3 audio. To get a link, open the chosen video on YouTube, use Share > Copy link, and paste the URL. Use links to videos you are permitted to share; do not extract audio from YouTube.
- This is a **local coursework project**, not production-ready. No accounts, permissions, or deployment hardening are included.
- A BST can become unbalanced; the implementation intentionally uses a plain BST, as required.
- Binary search comparison counts count midpoint duration checks. Adjacent equal-duration matches are gathered after the match is found.
- Adding/deleting songs changes database records and the BST is rebuilt on the next request. The algorithms read title/duration values from the database as they compare song IDs, trading extra database queries for not keeping temporary copies of those fields in the algorithm structures. This is simple for a 25+ song demonstration.
