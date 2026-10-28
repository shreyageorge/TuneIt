// Quick shorthand function to select DOM elements by their ID (like jQuery's $)
const $ = (id) => document.getElementById(id);

// Global application state variables
let songs = [];         
let playlists = [];    
let visible = [];       // Stores currently filtered/displayed songs
let current = -1;       // ID of the currently playing song
let view = 'home';      // Current active view mode ('home', 'library', etc.)
let activePlaylist = null; // ID of the currently selected playlist

// Grab audio element and set its default volume to 70%
const audio = $('audio');
audio.volume = 0.7;
// Grab YouTube dialog modal and iframe elements for video playback
const youtubeDialog = $('youtubeDialog');
const youtubeFrame = $('youtubeFrame');
let youtubeActive = false; // Tracks whether a YouTube video is currently playing

// --- Helper Functions ---

// Escapes special characters in strings to prevent Cross-Site Scripting (XSS)
function safe(s) {
  return String(s ?? '').replace(
    /[&<>"']/g,
    (c) =>
      ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
      }[c])
  );
}

// Converts seconds into a formatted MM:SS duration string
function duration(s) {
  return Math.floor(s / 60) + ':' + String(Math.floor(s % 60)).padStart(2, '0');
}

// Displays a temporary toast notification banner with a given message
function notice(msg) {
  $('toast').textContent = msg;
  $('toast').classList.add('show');
  setTimeout(() => $('toast').classList.remove('show'), 2600);
}

// Extracts and returns the Django CSRF token from browser cookies for secure POST requests
function csrf() {
  const x = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
  return x ? decodeURIComponent(x[1]) : '';
}

// Generic wrapper function to perform asynchronous API requests (GET/POST)
async function api(url, body) {
  const opts =
    body === undefined
      ? {}
      : {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf(),
          },
          body: JSON.stringify(body),
        };

  const res = await fetch(url, opts);
  const data = await res.json();
  if (!res.ok) throw Error(data.error || 'Request failed');
  return data;
}

// --- Data Loading & Navigation ---

// Fetches songs and playlists from the backend simultaneously, then updates the UI
async function load() {
  const [a, b] = await Promise.all([
    // api() function uses fetch() to communicate with Django. The load() function fetches
    // songs and playlists, then refreshes the interface.
    api('/api/songs/'),
    api('/api/playlists/'),
  ]);
  songs = a.songs;
  playlists = b.playlists;
  $('songCount').textContent = `${songs.length} songs`;
  renderNav();
  render();
}

// Renders dynamic playlist buttons in the sidebar and attaches click handlers to them
function renderNav() {
  $('playlistNav').innerHTML = playlists
    .map(
      (p) =>
        `<button class="playlist-link" data-playlist="${p.id}">♫ &nbsp; ${safe(p.name)}</button>`
    )
    .join('');

  document.querySelectorAll('[data-playlist]').forEach((b) => {
    b.onclick = () => {
      activePlaylist = Number(b.dataset.playlist);
      view = 'playlist';
      render();
    };
  });
}

// --- UI Components ---

// Generates HTML markup for an individual song grid card
function card(song) {
  return `
    <article class="card" data-song="${song.id}">
      <div class="cover">
        ${song.cover_url ? `<img src="${safe(song.cover_url)}" alt="">` : '♫'}
      </div>
      <strong>${safe(song.title)}</strong>
      <small>${safe(song.artist)} ·${duration(song.duration)}</small>
    </article>
  `;
}

// Generates HTML markup for a list of song rows (with add/remove playlist buttons)
function rows(items, playlistId = null) {
  return items
    .map(
      (s, i) => `
    <div class="song-row">
      <span class="muted">${i + 1}</span>
      <div class="title" data-song="${s.id}">
        <strong>${safe(s.title)}</strong>
      </div>
      <span class="artist muted">${safe(s.artist)}</span>
      <small>${duration(s.duration)}</small>
      <div>
        ${
          playlistId
            ? `<button data-remove="${s.id}">Remove</button>`
            : `<button data-add="${s.id}">＋ Playlist</button>`
        }
      </div>
    </div>
  `
    )
    .join('');
}

// Attaches click event listeners to song cards, play triggers, and playlist add/remove buttons
function wireSongs() {
  document.querySelectorAll('[data-song]').forEach((el) => {
    el.onclick = () => playSong(Number(el.dataset.song));
  });
  document.querySelectorAll('[data-add]').forEach((el) => {
    el.onclick = () => addPlaylistSong(Number(el.dataset.add));
  });
  document.querySelectorAll('[data-remove]').forEach((el) => {
    el.onclick = () => removePlaylistSong(Number(el.dataset.remove));
  });
}

// --- Main View Renderer ---

// Dynamically updates the main content area based on the current active 'view' state
function render() {
  const root = $('content');
  document.querySelectorAll('.nav').forEach((b) => {
    b.classList.toggle('active', b.dataset.view === view);
  });

  if (view === 'home') {
    $('viewName').textContent = 'Good evening';
    visible = songs;
    root.innerHTML = `
      <h1>Made for your music library</h1>
      <p class="sub">Discover your collection. Click a card to listen.</p>
      <h2>All songs</h2>
      <div class="grid">${songs.map(card