import numpy as np


class Point:
    def __init__(self, t_x, t_y):
        self.x = t_x
        self.y = t_y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)

    def __str__(self):
        return f"({self.x},{self.y})"

    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        return Point(x, y)

    def to_tuple(self) -> tuple:
        return self.x, self.y

    def distance(self, point) -> float:
        dis_p = self - point
        return np.linalg.norm(dis_p.to_tuple())


def get_point_from_angle_and_distance(angle: float, distance: float):
    x = np.round(np.cos(angle) * distance, 2)
    y = np.round(np.sin(angle) * distance, 2)
    return Point(x, y)
