from kivy.app import App as BaseApp
from kivy.base import EventLoop
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from world import World, get_size
from menu import StartMenu, GameMenu, ScoreMenu


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
        self._menu = None
        self._score_list = None
        self.open_menu('main')

    def exit(self, button):
        EventLoop.close()

    def open_menu(self, menu_name):
        if self._menu is not None:
            self.close_menu()
        if menu_name == 'main':
            kwargs = dict(main_widget=self,
                          spacing=20,
                          size=get_size((0.2, 0.5)))
            if self._world is None:
                menu = StartMenu(**kwargs)
            else:
                menu = GameMenu(**kwargs)
        elif menu_name == 'score':
            menu = ScoreMenu(main_widget=self, size=get_size((0.2, 0.6)))
        else:
            raise AssertionError('Unknown menu "{}"'.format(menu_name))
        self._menu = menu
        self.add_widget(menu)
        menu.center=self.center

    def close_menu(self):
        assert self._menu is not None
        self.remove_widget(self._menu)
        self._menu = None

    def open_score(self, button):
        self.open_menu('score')

    def open_main_menu(self, button):
        self.open_menu('main')

    def start_game(self, button):
        assert self._world is None
        self._world = World(color=S.world.background_color,
                            pos=(0, 0),
                            size=get_size(S.world.size))
        self.add_widget(self._world)
        self._world.bind(on_man_lost=self.incr_lost_score)
        self._world.bind(on_man_captured=self.incr_score)
        # setup score labels
        self._menu_btn_layout = AnchorLayout(size=self.size,
                                             anchor_x='left',
                                             anchor_y='top')
        self._menu_button = Button(text='Menu', size_hint=(0.1, 0.05))
        self._menu_button.bind(on_press=self.stop_game)
        self._menu_btn_layout.add_widget(self._menu_button)
        self.add_widget(self._menu_btn_layout)
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
        self.close_menu()

    def stop_game(self, button):
        self._world.stop_update()
        self._menu_button.unbind(on_press=self.stop_game)
        self.open_menu('main')

    def resume_game(self, button):
        self._world.start_update()
        self._menu_button.bind(on_press=self.stop_game)
        self.close_menu()

    def finish_game(self):
        assert self._world is not None
        self._world.destroy()
        self.remove_widget(self._world)
        self._world = None
        self.remove_widget(self._score_layout)
        self.remove_widget(self._menu_btn_layout)

    def restart(self, button):
        self.finish_game()
        self.start_game(button)

    def incr_lost_score(self, world, man):
        self._lost_score.current = self._lost_score.current + 1
        #TODO: check of game over

    def incr_score(self, world, man):
        self._score.current = self._score.current + 1

class App(BaseApp):

    def build(self):
        Builder.load_file('game.kv')
        return MainWidget(size=Window.size)
