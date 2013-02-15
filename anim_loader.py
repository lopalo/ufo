import os
from os.path import join, dirname
import json
from kivy.logger import Logger
from kivy.atlas import Atlas
from kivy.core.image import ImageLoaderBase, ImageLoader, Image as CoreImage
from kivy.properties import ListProperty

@ImageLoader.register
class AnimationAtlasLoader(ImageLoaderBase):

    def load(self, filename):
        return AnimAtlas(filename)

    def populate(self):
        self._textures = self._data.textures

    @property
    def width(self):
        return self.textures[0].width

    @property
    def height(self):
        return self.textures[0].height

    @property
    def size(self):
        return self.textures[0].size

    @staticmethod
    def extensions():
        return ('anim_atlas',)


class AnimAtlas(Atlas):
    textures = ListProperty([])

    def _load(self):
        filename = self._filename
        assert(filename.endswith('.anim_atlas'))
        filename = filename.replace('/', os.sep)

        Logger.debug('AnimAtlas: Load <%s>' % filename)
        with open(filename, 'r') as fd:
            meta = json.load(fd)

        d = dirname(filename)
        assert len(meta) == 1, ('AnimAtlas: <%s> should contain '
                                'info only for one image') % filename
        imagename, ids = next(meta.iteritems())

        reg_info = {}
        size = None
        for n, info in ids.items():
            if size is None:
                size = (info[2], info[3])
            elif info[2] != size[0] or info[3] != size[1]:
                raise ValueError('AnimAtlas: <%s> has parts '
                                 'with different sizes' % filename)
            reg_info[int(n)] = info

        imagename = join(d, imagename)
        Logger.debug('AnimAtlas: Load <%s>' % imagename)
        textures = []
        ci = CoreImage(imagename)
        for n in sorted(reg_info):
            textures.append(ci.texture.get_region(*reg_info[n]))

        self.textures = textures
