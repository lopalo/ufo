from random import choice
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.vector import Vector
from man import Man
from ufo import UFO
from anim_loader import on_anim_finish


def get_size(factor):
    return (int(Window.height * factor[0]),
            int(Window.height * factor[1]))


def get_pos(factor):
    return (int(Window.width * factor[0]),
            int(Window.height * factor[1]))

get_world_size = get_pos


class Rect(Widget):

    def __init__(self, **kwargs):
        self.color = kwargs['color']
        super(Rect, self).__init__(**kwargs)


class Ground(Rect):

    def __init__(self, **kwargs):
        self.line_color = kwargs['line_color']
        self.line_width = kwargs['line_width']
        super(Ground, self).__init__(**kwargs)


class World(Rect):

    def __init__(self, **kwargs):
        super(World, self).__init__(**kwargs)
        self.test_force = Vector(0, 0)
        self._ufo_direction = 0
        self._men = []
        self._objects = []
        self._elapsed_time = 0
        if S.ufo.control == 'arrows':
            keyboard = Window.request_keyboard(None, self)
            keyboard.bind(on_key_down=self.on_key_down,
                          on_key_up=self.on_key_up)
        self.ground = Ground(color=S.world.ground.color,
                             pos=(0, 0),
                             line_color=S.world.ground.border_color,
                             line_width=(S.world.ground.border_width *
                                                        Window.height),
                             size=get_world_size((S.world.size[0],
                                                  S.world.ground.height)))
        self.add_widget(self.ground)
        self._add_objects()
        self.ufo = UFO(center=(self.ground.center_x, Window.height * S.ufo.y),
                       source=S.ufo.image,
                       size=get_size(S.ufo.size),
                       anim_delay=1. / S.ufo.anim_speed,
                       ground=self.ground)
        self.add_widget(self.ufo)
        self.register_event_type('on_man_lost')
        self.register_event_type('on_man_captured')
        self.start_update()

        self._get_smoke() # need for caching

    def stop_update(self):
        Clock.unschedule(self.update)

    def start_update(self):
        Clock.schedule_interval(self.update, 1. / S.game.update_speed)

    def destroy(self):
        self.stop_update()

    def on_touch_down(self, touch):
        if S.ufo.control != 'touch_screen':
            return False
        if touch.x > Window.center[0]:
            self._ufo_direction = 1
        else:
            self._ufo_direction = -1
        return True

    def on_touch_up(self, touch):
        if S.ufo.control != 'touch_screen':
            return False
        if touch.x > Window.center[0] and self._ufo_direction > 0:
            self._ufo_direction = 0
        if touch.y <= Window.center[0] and self._ufo_direction < 0:
            self._ufo_direction = 0
        return True

    def on_key_down(self, keyboard, (code, kname), text, mod):
        if kname == 'f' and S.game.debug:
            self.test_force = Vector(S.game.test_force)
        if kname == 'right':
            self._ufo_direction = 1
        if kname == 'left':
            self._ufo_direction = -1

    def on_key_up(self, keyboard, (code, kname)):
        if kname == 'f' and S.game.debug:
            self.test_force = Vector(0, 0)
        if kname == 'right' and self._ufo_direction > 0:
            self._ufo_direction = 0
        if kname == 'left' and self._ufo_direction < 0:
            self._ufo_direction = 0

    def _add_objects(self):
        ww = Window.width * S.world.size[0]
        wh = Window.height * S.world.size[1]
        for n, obj in enumerate(S.world.objects):
            img = Image(source=obj['image'],
                        size=get_size(obj['size']),
                        pos=get_pos(obj['pos']))
            assert 0 <= img.right and ww >= img.x, ("Bad x coordinate "
                                                    "for {} item".format(n))
            assert 0 <= img.top and wh >= img.y, ("Bad y coordinate "
                                                "for {} item".format(n))

            self.add_widget(img)
            self._objects.append(img)

    def _add_man(self):
        gr = self.ground
        run_direction = choice([1, -1])
        img = S.man.right_image if run_direction == 1 else S.man.left_image
        x = gr.x if run_direction == 1 else gr.right
        man = Man(center=(x, gr.top),
                  source=img,
                  run_direction=run_direction,
                  size=get_size(S.man.size),
                  ground=gr)
        self.add_widget(man)
        self._men.append(man)

    def on_man_lost(self, man):
        self.remove_widget(man)
        self._men.remove(man)
        self.man_disappear(man)

    def on_man_captured(self, man):
        self.remove_widget(man)
        self._men.remove(man)
        self.man_disappear(man)

    def man_disappear(self, man):
        img = self._get_smoke()
        img.center_x = man.center_x
        img.y = man.y
        self.add_widget(img)
        self._objects.append(img)
        @on_anim_finish(img)
        def on_fin(img):
            self.remove_widget(img)
            self._objects.remove(img)

    def _get_smoke(self):
        s = S.man.disappear_animation
        return Image(source=s.image,
                     anim_delay = 1. / s.speed,
                     size=get_size(s.image_size))

    def update(self, dt):
        self._elapsed_time += dt
        step = int(self._elapsed_time / S.game.step) + 1
        need_men = int(step * S.game.increment_men_on_step)
        diff = need_men - len(self._men)
        for _ in range(diff):
            self._add_man()
        ufo = self.ufo
        ufo.update(dt, self._ufo_direction)
        self._update_screen()
        force = Vector(0, -S.world.gravity) + self.test_force
        for man in self._men:
            fdir = ufo.in_ray(man)
            if fdir is not None:
                iforce = force + fdir * S.ufo.ray.force
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
        for obj in self._objects:
            obj.x += d



