from math import cos, sin, radians, degrees, copysign
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, NumericProperty
from kivy.graphics import Color, Line
from kivy.vector import Vector


class UFO(Image):
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        from world import get_size

        super(UFO, self).__init__(**kwargs)
        self._ground = kwargs['ground']
        self._speed = 0
        self._pendulum = Pendulum()
        ray = Ray(ufo=self,
                  size=get_size(S.ufo.ray.size),
                  anim_delay=1. / S.ufo.ray.anim_speed,
                  source=S.ufo.ray.image)
        self.add_widget(ray)
        self.bind(x=ray.update, angle=ray.update)

    def in_ray(self, man):
        v = Vector(man.center) - Vector(self.center)
        direction = Vector(1, 0).rotate(self.angle - 90)
        angle = abs(direction.angle(v))
        if angle <= S.ufo.ray.angle / 2.:
            return v.normalize().rotate(180)

    def update(self, dt, move_direction):
        self._speed += S.ufo.acceleration / dt * move_direction
        if not move_direction:
            sign = copysign(1, self._speed)
            self._speed -= S.ufo.braking / dt * sign
            if sign != copysign(1, self._speed):
                self._speed = 0
        max_speed = S.ufo.max_speed * self.width # absolute value
        self._speed = max(min(self._speed, max_speed), -max_speed)
        self.x += self.width * self._speed * dt
        self.right = min(self.right, self._ground.right)
        self.x = max(self.x, self._ground.x)

        pendulum = self._pendulum
        pendulum.update(dt, move_direction)
        self.angle = pendulum.angle


class Pendulum(object):

    def __init__(self, start_angle=0):
        self.angle = start_angle #vertical angle
        self._speed = 0

    def update(self, dt, move_direction):
        s = S.ufo.pendulum
        ra = radians(self.angle)
        f = -move_direction * cos(ra) * s.swing_factor
        gf = -sin(ra) * s.gravity_factor
        self._speed += (f + gf) * dt
        if not move_direction:
            sign = copysign(1, self._speed)
            self._speed -= s.braking_factor / dt * sign
        self.angle += self._speed * dt
        if self.angle > s.amplitude_angle:
            self.angle = s.amplitude_angle
            self._speed = 0
        elif self.angle < -s.amplitude_angle:
            self.angle = -s.amplitude_angle
            self._speed = 0


class Ray(Image):

    def __init__(self, **kwargs):
        self.ufo = kwargs['ufo']
        super(Ray, self).__init__(**kwargs)
        if not S.game.debug:
            return
        with self.canvas:
            Color(1, 1, 1)
            self._rline = Line()
            self._lline = Line()

    def update(self, ufo, val):
        if not S.game.debug:
            return
        v = Vector(0, -1)
        rv = v.rotate(S.ufo.ray.angle / 2.) * ufo.y + Vector(ufo.center)
        lv = v.rotate(S.ufo.ray.angle / -2.) * ufo.y + Vector(ufo.center)
        self._rline.points = ufo.center + rv
        self._lline.points = ufo.center + lv
