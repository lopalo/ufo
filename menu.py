from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class MainMenu(BoxLayout):

    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.post_init(kwargs['main_widget'])

    def add_buttons(self, mw):
        button = Button(text='Score')
        self.add_widget(button)

        button = Button(text='Exit')
        button.bind(on_press=mw.exit)
        self.add_widget(button)

    def post_init(self, mw):
        self.add_widget(Label(text='UFO', font_size='30sp'))
        self.add_buttons(mw)


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

