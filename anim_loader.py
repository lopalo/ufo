from kivy.atlas import Atlas
from kivy.core.image import ImageLoaderBase, ImageLoader, Image as CoreImage

@ImageLoader.register
class AnimationAtlasLoader(ImageLoaderBase):

    def load(self, filename):
        return Atlas(filename)

    def populate(self):
        txts = dict((int(k), v) for k, v in self._data.textures.items())
        self._textures = [txts[p] for p in sorted(txts)]

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
        return ('atlas',)

