from kivy.app import App as BaseApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from world import World, get_size


class Score(Label):

    def __init__(self, pattern, current=0, max=None, **kwargs):
        self._current = current
        self._max = max
        self._pattern = pattern
        text = pattern.format(current=current, max=max)
        super(Score, self).__init__(text=text, **kwargs)

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, val):
        self._current = val
        self.text = self._pattern.format(current=self._current, max=self._max)


class MainWidget(Widget):

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self._world = None
        #TODO: start from menu
        self.start_game()

    def start_game(self):
        self._world = World(color=S.world.background_color,
                            pos=(0, 0),
                            size=get_size(S.world.size))
        self.add_widget(self._world)
        self._world.bind(on_man_lost=self.incr_lost_score)
        self._world.bind(on_man_captured=self.incr_score)
        # setup score labels
        self._score_layout = AnchorLayout(size=self.size,
                                          anchor_x='right',
                                          anchor_y='top')
        score_box = BoxLayout(orientation='vertical', size_hint=(0.2, 0.1))
        self._score_layout.add_widget(score_box)
        self.add_widget(self._score_layout)
        self._score = Score(pattern='Score: {current}')
        score_box.add_widget(self._score)
        self._lost_score = Score(pattern='Lost: {current}/{max}',
                                 max=S.game.max_dead_men)
        score_box.add_widget(self._lost_score)

    def stop_game(self):
       self._world.stop_update()

    def resume_game(self):
        self._world.start_update()

    def finish_game(self):
        self._world.destroy()
        self.remove_widget(self._world)
        self._world = None
        self.remove_widget(self._score_layout)

    def incr_lost_score(self, world, man):
        self._lost_score.current = self._lost_score.current + 1
        #TODO: check of game over

    def incr_score(self, world, man):
        self._score.current = self._score.current + 1

class App(BaseApp):

    def build(self):
        Builder.load_file('game.kv')
        return MainWidget(size=Window.size)
