from os import path
import yaml
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


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


def get_score():
    if path.exists(S.game.score.file):
        with open(S.game.score.file, 'r') as f:
            return yaml.load(f)['score']
    return []


class ScoreMenu(BoxLayout):

    def __init__(self, **kwargs):
        super(ScoreMenu, self).__init__(**kwargs)
        self.orientation = 'vertical'
        score = get_score()
        score.sort(key=lambda i: i[1], reverse=True)
        color = S.game.score.color
        self.add_widget(Label(text='Score', font_size='30sp', color=color))
        for name, sc in score[:10]:
            self.add_widget(Label(text=u'{}: {}'.format(name, sc),
                                  color=color,
                                  font_size='20sp'))
        button = Button(text='Menu')
        button.bind(on_press=kwargs['main_widget'].open_main_menu)
        self.add_widget(button)


class EnterName(BoxLayout):

    def __init__(self, **kwargs):
        super(EnterName, self).__init__(**kwargs)
        self._score = kwargs['score']
        self._main_widget = kwargs['main_widget']

        self.orientation = 'vertical'
        self.add_widget(Label(text='Enter name', font_size='20sp'))
        self._text_input = TextInput(multiline=False)
        self.add_widget(self._text_input)
        button = Button(text='Ok')
        button.bind(on_press=self.ok)
        self.add_widget(button)

    def ok(self, button):
        score = get_score()
        with open(S.game.score.file, 'wb') as f:
            name = self._text_input.text
            score.append([name, self._score])
            score.sort(key=lambda i: i[1], reverse=True)
            score = score[:10]
            yaml.dump({'score': score}, f, allow_unicode=True)
        self._main_widget.open_main_menu(button)

