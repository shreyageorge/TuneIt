"""Run: python manage.py shell -c 'from music.seed import seed; seed()'"""
from .models import Song

TRACKS = [
    ('Billie Jean', 'Michael Jackson', 294, 'Zi_XLOBDo_Y'),
    ('Bohemian Rhapsody', 'Queen', 354, 'fJ9rUzIMcZQ'),
    ('Smells Like Teen Spirit', 'Nirvana', 278, 'hTWKbfoikeg'),
    ('Take On Me', 'a-ha', 228, 'djV11Xbc914'),
    ('Never Gonna Give You Up', 'Rick Astley', 213, 'dQw4w9WgXcQ'),
    ('Shape of You', 'Ed Sheeran', 264, 'JGwWNGJdvx8'),
    ('Hello', 'Adele', 367, 'YQHsXMglC9A'),
    ('Uptown Funk', 'Mark Ronson ft. Bruno Mars', 271, 'OPf0YbXqDm0'),
    ('Rolling in the Deep', 'Adele', 234, 'rYEDA3JcQqw'),
    ('Blinding Lights', 'The Weeknd', 262, '4NRXx6U8ABQ'),
    ('Viva La Vida', 'Coldplay', 243, 'dvgZkm1xWPE'),
    ('Believer', 'Imagine Dragons', 217, '7wtfhZwyrcc'),
    ('Bad Romance', 'Lady Gaga', 309, 'qrO4YZeyl0I'),
    ('Firework', 'Katy Perry', 235, 'QGJuMBdaqIw'),
    ('Counting Stars', 'OneRepublic', 284, 'hT_nvWreIhg'),
    ('Shake It Off', 'Taylor Swift', 242, 'nfWlot6h_JM'),
    ("Don't Start Now", 'Dua Lipa', 183, 'oygrmJFKYZY'),
    ('Roar', 'Katy Perry', 270, 'CevxZvSJLk8'),
    ('Clocks', 'Coldplay', 254, 'd020hcWA_Wg'),
    ('Numb', 'Linkin Park', 187, 'kXYiU_JCYtU'),
    ('Someone Like You', 'Adele', 285, 'hLQl3WQQoQ0'),
    ('Toxic', 'Britney Spears', 211, 'LOZuxwVk7TU'),
    ('Wonderwall', 'Oasis', 278, '6hzrDeceEKc'),
    ('Africa', 'Toto', 262, 'FTQbiNvZqaY'),
    ("Sweet Child O' Mine", "Guns N' Roses", 356, '1w7OgIMMRc4'),
    ('Seven Nation Army', 'The White Stripes', 239, '0J2QdDbelmY'),
    ('Lose Yourself', 'Eminem', 323, 'xFYQQPAOz7Y'),
]

LEGACY_DEMO_TITLES = (
    'Midnight Drive', 'Golden Hour', 'Ocean Lights', 'City Rain', 'Afterglow',
    'Starlight', 'Blue Horizon', 'Quiet Streets', 'Neon Dreams', 'Summer Echo',
    'Northern Sky', 'Silver Moon', 'Daybreak', 'Slow Motion', 'Electric Heart',
    'Cloud Nine', 'Falling Leaves', 'Paper Planes', 'Moonflower', 'Waves of Time',
    'Velvet Night', 'Open Road', 'Last Train', 'Distant Stars', 'First Light',
    'Crystal Lake', 'Echo Valley',
)


def seed():
    old_songs = list(
        Song.objects.filter(title__in=LEGACY_DEMO_TITLES).order_by('id')
    )
    for song, track in zip(old_songs, TRACKS):
        title, artist, duration, youtube_id = track
        song.title = title
        song.artist = artist
        song.duration = duration
        song.audio_url = f'https://www.youtube.com/watch?v={youtube_id}'
        song.save(update_fields=['title', 'artist', 'duration', 'audio_url'])

    for title, artist, duration, youtube_id in TRACKS:
        #This looks for an existing song with that title. If the song exists, it leaves it alone; otherwise, it creates the record.
        Song.objects.update_or_create(
            title=title,
            defaults={
                'artist': artist,
                'duration': duration,
                'audio_url': f'https://www.youtube.com/watch?v={youtube_id}',
            },
        )
    print('Seeded', Song.objects.count(), 'songs')
