from math import cos, sin, radians
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Line
from kivy.vector import Vector

class UFO(Widget):
    direction = ObjectProperty(Vector(0, -1))

    def __init__(self, **kwargs):
        super(UFO, self).__init__(**kwargs)
        self._ground = kwargs['ground']
        if S.game.debug:
            self._ray = Ray(ufo=self)
            self.add_widget(self._ray)
            self.bind(x=self._ray.update, direction=self._ray.update)

    def to_right(self):
        self.x += self.width * 0.1
        self.right = min(self.right, self._ground.right)

    def to_left(self):
        self.x -= self.width * 0.1
        self.x = max(self.x, self._ground.x)

    def in_ray(self, man):
        v = Vector(man.center) - Vector(self.center)
        angle = abs(self.direction.angle(v))
        if angle <= S.ufo.ray_angle / 2.:
            return v.normalize().rotate(180)



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
        rv = v.rotate(S.ufo.ray_angle / 2.) * ufo.y + Vector(ufo.center)
        lv = v.rotate(S.ufo.ray_angle / -2.) * ufo.y + Vector(ufo.center)
        self._rline.points = ufo.center + rv
        self._lline.points = ufo.center + lv
