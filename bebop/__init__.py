from __future__ import print_function

from scription import *
from antipathy import Path
from tinytag import TinyTag, TinyTagException


@Command(
        song=Spec('song file to play', ),
        )
def play(song):
    from playsound import playsound
    tags = TinyTag.get(song)
    # text = []
    # text.append('album: %s' % tags['album'])
    # text.append('artist: %s' % tags['artist'])
    print('album: %s     artist: %s' % (tags['album'], tags['artist']), border='box')
    playsound(song)


@Command(
        source=Spec('source location to scan for music files', type=Path),
        destination=Spec('target for unique songs', type=Path),
        )
def merge(source, destination):
    """
    ensures DESTINATION has a single copy of each song; .m4a format preferred
    """
    # DESTINATION
    #            / <album>
    #                      / song
    for path, dirs, files in source.walk():
        files.sort(key=lambda f: f.ext)
        for song in files:
            print('%s ...  ' % song, end='', verbose=2)
            source_song = path/song
            # if TinyTag cannot parse it, assume not a song and move on
            try:
                tags = TinyTag.get(source_song)
            except TinyTagException as e:
                print('skipping', verbose=2)
                continue
            album = clean_path(tags.album) or clean_path(tags.artist) or clean_path(tags.title) or 'Unknown'
            target = destination/album
            try:
                target.makedirs()
            except OSError as e:
                album = 'Unknown'
                target = destination/album
                try:
                    target.makedirs()
                except OSError:
                    print(e, '-- skipping')
                    continue
            target_name = clean_path(tags.title)
            target_ext = song.ext
            target_song = target/target_name+target_ext
            files = target.glob(target_name+'.*')
            if len(files) > 1:
                raise ValueError('too many copies of %r in %r\n%r' % (target_name, target, files))
            if files:
                if challenger_wins(files[0], tags):
                    Path(files[0]).unlink()
                else:
                    print('already exists', verbose=2)
                    continue
            print('copying to %s' % target_song, verbose=2)
            try:
                source_song.copy(target_song)
            except PermissionError:
                # some file systems don't allow changing metadata
                pass





# helpers

def challenger_wins(existing, challenger_tags):
    """
    uses bitrate, channels, and duration to choose winner
    """
    existing_tags = et = TinyTag.get(existing)
    ct = challenger_tags
    if ct.bitrate and et.bitrate:
        if ct.bitrate < et.bitrate:
            return False
        if ct.bitrate > et.bitrate:
            return True
    if ct.channels and et.channels:
        if ct.channels < et.channels:
            return False
        if ct.channels > et.channels:
            return True
    if ct.duration and et.duration:
        if ct.duration < et.duration + 2:
            return False
        if ct.duration > et.duration + 2:
            return True
    return False

def clean_path(name):
    if name is None:
        return ''
    return name.replace(':','- ').replace(';',' -').replace('"','_').replace('/',' and ').replace('?','').replace('*','').replace('.','').strip()


# do it

Run()
