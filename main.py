import __builtin__
import yaml
import kivy
kivy.require('1.5.1')
from anim_loader import AnimationAtlasLoader #registers loader for Image


class Settings(object):


    def __init__(self, dct, is_root):
        self.__dict__.update(dct)
        self._root = is_root

    @classmethod
    def load_yaml(cls, filename):
        with open(filename, 'rb') as f:
            dct = yaml.load(f)
            return cls(dct, True)

    def __getattribute__(self, name):
        val = super(Settings, self).__getattribute__(name)
        if not name.startswith('_') and isinstance(val, dict):
            return self.__class__(val, False)
        return val


if __name__ == '__main__':
    __builtin__.S = Settings.load_yaml('settings.yaml')
    if S.game.fullscreen:
        from kivy.config import Config
        Config.set('graphics', 'fullscreen', 'auto')
    from game_app import App
    App().run()

