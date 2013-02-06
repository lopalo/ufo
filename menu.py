from os import path
import yaml
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class MainMenu(BoxLayout):

    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.add_widget(Label(text='UFO', font_size='30sp'))
        self.add_buttons(kwargs['main_widget'])

    def add_buttons(self, mw):
        button = Button(text='Score')
        button.bind(on_press=mw.open_score)
        self.add_widget(button)

        button = Button(text='Exit')
        button.bind(on_press=mw.exit)
        self.add_widget(button)


class StartMenu(MainMenu):

    def add_buttons(self, mw):
        button = Button(text='Start')
        button.bind(on_press=mw.start_game)
        self.add_widget(button)
        super(StartMenu, self).add_buttons(mw)


class GameMenu(MainMenu):

    def add_buttons(self, mw):
        button = Button(text='Resume')
        button.bind(on_press=mw.resume_game)
        self.add_widget(button)

        button = Button(text='Restart')
        button.bind(on_press=mw.restart)
        self.add_widget(button)
        super(GameMenu, self).add_buttons(mw)


class ScoreMenu(BoxLayout):

    def __init__(self, **kwargs):
        super(ScoreMenu, self).__init__(**kwargs)
        self.orientation = 'vertical'
        if path.exists(S.game.score_file):
            with open(S.game.score_file, 'rb') as f:
                score = yaml.load(f)['score']
        else:
            score = []
        score.sort(key=lambda i: i[0])
        color = S.game.score_color
        self.add_widget(Label(text='Score', font_size='30sp', color=color))
        for name, sc in score[:10]:
            self.add_widget(Label(text='{}: {}'.format(name, sc),
                                  color=color,
                                  font_size='20sp'))
        button = Button(text='Menu')
        button.bind(on_press=kwargs['main_widget'].open_main_menu)
        self.add_widget(button)



