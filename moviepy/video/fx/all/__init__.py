"""
Loads all the fx !
Usage:
import moviepy.video.fx.all as vfx
clip = vfx.resize(some_clip, width=400)
clip = vfx.mirror_x(some_clip)
"""

import pkgutil
import moviepy.video.fx as fx

__all__ = [name for _, name, _ in pkgutil.iter_modules(
    fx.__path__) if name != "all"]

#focr name in __all__:
    #exec("from ..%s import %s" % (name, name))
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
