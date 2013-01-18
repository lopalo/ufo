from random import choice
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.vector import Vector
from man import Man
from ufo import UFO


def get_size(size_factor):
    return (int(Window.width * size_factor[0]),
            int(Window.height * size_factor[1]))


class Rect(Widget):

    def __init__(self, **kwargs):
        self.color = kwargs['color']
        super(Rect, self).__init__(**kwargs)


class World(Rect):

    def __init__(self, **kwargs):
        super(World, self).__init__(**kwargs)
        self.test_force = Vector(0, 0)
        self._ufo_direction = 0
        self._men = []
        self._elapsed_time = 0
        keyboard = Window.request_keyboard(None, self)
        keyboard.bind(on_key_down=self.on_key_down, on_key_up=self.on_key_up)
        self.ground = Rect(color=S.world.ground_color,
                           pos=(0, 0),
                           size=get_size((S.world.size[0],
                                          S.world.ground_height)))
        self.add_widget(self.ground)
        self.ufo = UFO(center=(self.ground.center_x, Window.height * S.ufo.y),
                       size=get_size((S.ufo.size)),
                       ground=self.ground)
        self.add_widget(self.ufo)
        self.register_event_type('on_man_lost')
        self.register_event_type('on_man_captured')
        self.start_update()

    def stop_update(self):
        Clock.unschedule(self.update)

    def start_update(self):
        Clock.schedule_interval(self.update, 1. / S.game.update_speed)

    def destroy(self):
        self.stop_update()
        keyboard.unbind(on_key_down=self.on_key_down,
                        on_key_up=self.on_key_up)

    def on_key_down(self, keyboard, (code, kname), text, mod):
        if kname == 'f' and S.game.debug:
            self.test_force = Vector(S.game.test_force)
        if S.ufo.control == 'arrows':
            if kname == 'right':
                self._ufo_direction = 1
            if kname == 'left':
                self._ufo_direction = -1

    def on_key_up(self, keyboard, (code, kname)):
        if kname == 'f' and S.game.debug:
            self.test_force = Vector(0, 0)
        if S.ufo.control == 'arrows':
            if kname == 'right' and self._ufo_direction > 0:
                self._ufo_direction = 0
            if kname == 'left' and self._ufo_direction < 0:
                self._ufo_direction = 0

    def add_man(self):
        gr = self.ground
        run_direction = choice([1, -1])
        img = S.man.right_image if run_direction == 1 else S.man.left_image
        x = gr.x if run_direction == 1 else gr.right
        man = Man(center=(x, gr.top),
                  source=img,
                  run_direction=run_direction,
                  size=get_size((S.man.size, S.man.size)),
                  ground=gr)
        self.add_widget(man)
        self._men.append(man)

    def on_man_lost(self, man):
        self.remove_widget(man)
        self._men.remove(man)

    def on_man_captured(self, man):
        self.remove_widget(man)
        self._men.remove(man)

    def update(self, dt):
        self._elapsed_time += dt
        step = int(self._elapsed_time / S.game.step) + 1
        need_men = int(step * S.game.increment_men_on_step)
        diff = need_men - len(self._men)
        for _ in range(diff):
            self.add_man()
        ufo = self.ufo
        if self._ufo_direction == 1:
            ufo.to_right()
        elif self._ufo_direction == -1:
            ufo.to_left()
        self._update_screen()
        force = Vector(0, -S.world.gravity) + self.test_force
        for man in self._men:
            fdir = ufo.in_ray(man)
            if fdir is not None:
                iforce = force + fdir * S.ufo.ray_force
                man.update(iforce, dt)
            else:
                man.update(force, dt)
            x, y = man.center
            if ufo.x < x < ufo.right and ufo.y < y < ufo.top:
                self.dispatch('on_man_captured', man)


    def _update_screen(self):
        x = self.x
        diff = Window.center[0] - self.ufo.center_x
        self.x += diff
        self.x = min(self.x, 0)
        self.right = max(self.right, Window.width)
        d = self.x - x
        self.ground.x += d
        self.ufo.x += d
        for man in self._men:
            man.x += d




