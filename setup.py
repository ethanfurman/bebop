try:
    import setuptools
except ImportError:
    pass
from distutils.core import setup
import sys

long_desc = '''\
=====
bebop
=====

Synopsis
========

*bebop* is a cataloging music player.  It's important distinctions are:

- random mode:  it makes sure that every song is played in a list before any song is repeated
  (with some adjustments for favorites) -- after all, if have a song in a list you want to hear
  it, right?

- *playlist*/*genre*: playlists and genres are tracked by tag -- *country* and *upbeat* would
  both be tags, and both selectable as playlists

- favorites: each song has a favorites rating *by tag* -- meaning a song can have a high
  rating in one tag (and be played more often there) and a low rating in a different tag (so
  it's not played as often when that tag is selected)
'''

data = dict(
       name='bebop',
       version='0.0.0.1a',
       url='https://github.com/ethanfurman/bebop',
       packages=['bebop'],
       package_data={
           'bebop' : [
               'LICENSE',
               'README',
               # 'doc/bebop.rst',
               # 'doc/bebop.pdf',
               ]
           },
       include_package_data=True,
       license='BSD License (2-clause)',
       description="music player with intelligent randomizer",
       long_description=long_desc,
       provides=['bebop'],
       author='Ethan Furman',
       author_email='ethan@stoneleaf.us',
       classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Topic :: Games/Entertainment',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            ],
    )

py2_only = ()
py3_only = ()
make = [
        # 'rst2pdf bebop/doc/bebop.rst --output=bebop/doc/bebop.pdf',
        ]

if __name__ == '__main__':
    if 'install' in sys.argv:
        import os, sys
        if sys.version_info[0] != 2:
            for file in py2_only:
                try:
                    os.unlink(file)
                except OSError:
                    pass
        if sys.version_info[0] != 3:
            for file in py3_only:
                try:
                    os.unlink(file)
                except OSError:
                    pass
    setup(**data)
