from random import choice, random
from kivy.uix.image import Image
from kivy.vector import Vector
from kivy.properties import NumericProperty


class Man(Image):
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Man, self).__init__(**kwargs)
        self._ground = kwargs['ground']
        self._run_direction = kwargs['run_direction']
        diff = S.man.dspeed * random()
        self._run_speed = S.man.speed + diff
        self._set_run()

    def _set_run(self):
        self._in_air = False
        self.y = self._ground.top
        self._fly_rotation_direction = None
        self.angle = 0
        self._fly_speed = Vector(0, 0)
        self.anim_delay = 1. / (S.man.speed * 500.)

    def update(self, force, dt):
        self._update_state(force)
        if self._in_air:
            self._update_fly(force, dt)
        else:
            self._update_run()
        if (self.center_x < self._ground.x or
            self.center_x > self._ground.right):
            if S.game.debug:
                if self.center_x < self._ground.x:
                    self.center_x = self._ground.right
                else:
                    self.center_x = self._ground.x
            else:
                self.parent.dispatch('on_man_lost', self)

    def _update_state(self, force):
        if not self._in_air and force.y > 0:
            self._in_air = True
            self._fly_rotation_direction = choice([1, -1])
            self.anim_delay = -1

        if self._in_air and self.y < self._ground.top:
            speed = self._fly_speed.length() * self.height
            if speed >= S.man.deadly_fly_speed:
                self.parent.dispatch('on_man_lost', self)
            else:
                self._set_run()


    def _update_fly(self, force, dt):
        # mass = 1 and therefore force = acceleration
        self.y = float(self.y)
        self._fly_speed += force * dt
        diff = self._fly_speed * dt * self.height
        self.x += diff.x
        self.y += diff.y
        adiff = float(S.man.fly_rotation_speed) * dt
        self.angle += adiff * self._fly_rotation_direction

    def _update_run(self):
        self.x += self.width * self._run_speed * self._run_direction

