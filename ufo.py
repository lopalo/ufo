from math import cos, sin, radians, copysign
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Line
from kivy.vector import Vector

class UFO(Widget):
    direction = ObjectProperty(Vector(0, -1))

    def __init__(self, **kwargs):
        super(UFO, self).__init__(**kwargs)
        self._ground = kwargs['ground']
        self._speed = 0
        if S.game.debug:
            self._ray = Ray(ufo=self)
            self.add_widget(self._ray)
            self.bind(x=self._ray.update, direction=self._ray.update)

    def in_ray(self, man):
        v = Vector(man.center) - Vector(self.center)
        angle = abs(self.direction.angle(v))
        if angle <= S.ufo.ray.angle / 2.:
            return v.normalize().rotate(180)

    def update(self, dt, direction):
        if direction:
            self._speed += S.ufo.acceleration / dt * direction
        else:
            sign = copysign(1, self._speed)
            self._speed -= S.ufo.braking / dt * sign
            if sign != copysign(1, self._speed):
                self._speed = 0
        max_speed = S.ufo.max_speed * self.width # absolute value
        self._speed = max(min(self._speed, max_speed), -max_speed)
        self.x += self.width * self._speed * dt
        self.right = min(self.right, self._ground.right)
        self.x = max(self.x, self._ground.x)

class Ray(Widget):
    #need for debugging

    def __init__(self, **kwargs):
        super(Ray, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1)
            self._rline = Line()
            self._lline = Line()

    def update(self, ufo, val):
        v = ufo.direction
        rv = v.rotate(S.ufo.ray.angle / 2.) * ufo.y + Vector(ufo.center)
        lv = v.rotate(S.ufo.ray.angle / -2.) * ufo.y + Vector(ufo.center)
        self._rline.points = ufo.center + rv
        self._lline.points = ufo.center + lv
