"""
This file is meant to make it easy to load the main features of
MoviePy by simply typing:

>>> from moviepy.editor import *

In particular it will load many effects from the video.fx and audio.fx
folders and turn them into VideoClip methods, so that instead of
>>> clip.fx( vfx.resize, 2 ) # or equivalently vfx.resize(clip, 2)
we can write
>>> clip.resize(2)

It also starts a PyGame session (if PyGame is installed) and enables
clip.preview().
"""

# Note that these imports could have been performed in the __init__.py
# file, but this would make the loading of moviepy slower.

import os
import sys

# Downloads ffmpeg if it isn't already installed
import imageio
# Checks to see if the user has set a place for their own version of ffmpeg

if os.getenv('FFMPEG_BINARY', 'ffmpeg-imageio') == 'ffmpeg-imageio':
    if sys.version_info < (3, 4):
        #uses an old version of imageio with ffmpeg.download.
        imageio.plugins.ffmpeg.download()

# Clips
from .video.io.VideoFileClip import VideoFileClip
from .video.io.ImageSequenceClip import ImageSequenceClip
from .video.io.downloader import download_webfile
from .video.VideoClip import VideoClip, ImageClip, ColorClip, TextClip
from .video.compositing.CompositeVideoClip import CompositeVideoClip, clips_array
from .video.compositing.concatenate import concatenate_videoclips, concatenate # concatenate=deprecated

from .audio.AudioClip import AudioClip, CompositeAudioClip, concatenate_audioclips
from .audio.io.AudioFileClip import AudioFileClip

# FX

#import moviepy.video.fx.all as vfx
#import moviepy.audio.fx.all as afx
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.volumex import volumex
from moviepy.video.fx.crop import crop
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
#from moviepy.video.fx.left_right import left_right
from moviepy.video.fx.margin import margin
from moviepy.video.fx.loop import loop
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize

#import moviepy.video.compositing.transitions as transfx
from moviepy.video.compositing.transitions import crossfadein
from moviepy.video.compositing.transitions import crossfadeout

# Tools

import moviepy.video.tools as videotools
import moviepy.video.io.ffmpeg_tools as ffmpeg_tools
from .video.io.html_tools import ipython_display
from .tools import cvsecs

try:
    from .video.io.sliders import sliders
except ImportError:
    pass

# The next loop transforms many effects into VideoClip methods so that
# they can be walled with myclip.resize(width=500) instead of 
# myclip.fx( vfx.resize, width= 500)
for method in [
          #"afx.audio_fadein",
          #"afx.audio_fadeout",
          #"afx.audio_normalize",
          #"afx.volumex",
          "audio_fadein",
          "audio_fadeout",
          "audio_normalize",
          "volumex",
          #"transfx.crossfadein",
          #"transfx.crossfadeout",
          "crossfadein",
          "crossfadeout",
          #"vfx.crop",
          #"vfx.fadein",
          #"vfx.fadeout",
          #"vfx.invert_colors",
          #"vfx.loop",
          #"vfx.margin",
          #"vfx.mask_and",
          #"vfx.mask_or",
          #"vfx.resize",
          #"vfx.rotate",
          #"vfx.speedx"
          "crop",
          "fadein",
          "fadeout",
          "invert_colors",
          "loop",
          "margin",
          "mask_and",
          "mask_or",
          "resize",
          "rotate",
          "speedx"
          ]:

    exec("VideoClip.%s = %s" % (method, method))


for method in ["audio_fadein",
               "audio_fadeout",
               "audio_loop",
               "audio_normalize",
               "volumex"
              ]:
              
    exec("AudioClip.%s = %s" % (method, method))


# adds easy ipython integration
VideoClip.ipython_display = ipython_display
AudioClip.ipython_display = ipython_display
#-----------------------------------------------------------------
# Previews: try to import pygame, else make methods which raise
# exceptions saying to install PyGame


# Add methods preview and show (only if pygame installed)
try:
    from moviepy.video.io.preview import show, preview
except ImportError:
    def preview(self, *args, **kwargs):
        """NOT AVAILABLE : clip.preview requires Pygame installed."""
        raise ImportError("clip.preview requires Pygame installed")

    def show(self, *args, **kwargs):
        """NOT AVAILABLE : clip.show requires Pygame installed."""
        raise ImportError("clip.show requires Pygame installed")


VideoClip.preview = preview
VideoClip.show = show

try:
    from moviepy.audio.io.preview import preview
except ImportError:
    def preview(self, *args, **kwargs):
        """ NOT AVAILABLE : clip.preview requires Pygame installed."""
        raise ImportError("clip.preview requires Pygame installed")

AudioClip.preview = preview
