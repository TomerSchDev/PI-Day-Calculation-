from point import *
import numpy as np

import pygame

WIDTH = 1920
HEIGHT = 1080

CENTER = Point(WIDTH // 2, HEIGHT // 2)


def transformToScreen(point: Point) -> Point:
    return point + CENTER


def calculate_polygon_radius(inner_circle_radius, num_vertices):
    # Calculate the radius of the larger circle such that it touches all vertices of the polygon
    # This is essentially the distance from the origin to the farthest vertex
    # The farthest vertex occurs at pi/num_vertices away from the x-axis
    return inner_circle_radius / np.cos(np.deg2rad(TOTAL_ANGLES / (2 * num_vertices)))


def calculate_points(num_edges):
    inside_points = []
    outside_points = []
    polygon_radius = calculate_polygon_radius(RADIOS, num_edges)
    angle_between_points = TOTAL_ANGLES / num_edges
    for i in range(num_edges):
        angle = np.deg2rad(i * angle_between_points)
        p = get_point_from_angle_and_distance(angle, RADIOS)
        inside_points.append(p)
        # outside_point
        new_angle = np.deg2rad((i + 1) * angle_between_points)
        outside_points.append(get_point_from_angle_and_distance(new_angle, polygon_radius))
    return inside_points, outside_points


# ouside_len = 2*R *4
# pi > inside /2*R
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
RADIOS = 300
TOTAL_ANGLES = 360.0
keepGameRunning = True
num_edges = 4
font = pygame.font.SysFont("comicsansms", 35)
key_down = False
inside_points, outside_points = calculate_points(num_edges)
while keepGameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGameRunning = False
        elif event.type == pygame.KEYDOWN and not key_down:
            key_down = True
            if event.key == pygame.K_RIGHT:
                num_edges += 1
            elif event.key == pygame.K_LEFT:
                num_edges = max(3, num_edges - 1)
            elif event.key == pygame.K_SPACE:
                debug = True
            inside_points, outside_points = calculate_points(num_edges)
        elif event.type == pygame.KEYUP:
            key_down = False

    window.fill("white")
    pygame.draw.circle(window, (0, 0, 0), CENTER.to_tuple(), RADIOS, 10)
    dis_sum = 0
    outside_sum = 0
    for i, c in enumerate(outside_points):
        new_point = transformToScreen(c)
        o_p=outside_points[i - 1]
        old_p = transformToScreen(o_p)
        pygame.draw.circle(window, (150, 150, 0), new_point.to_tuple(), 10)
        pygame.draw.line(window, (255, 0, 0), new_point.to_tuple(), old_p.to_tuple(), 5)
        outside_sum += o_p.distance(c)
    for i, p in enumerate(inside_points):
        new_point = transformToScreen(p)
        pygame.draw.circle(window, (255, 0, 0), new_point.to_tuple(), 10)
        point_before = inside_points[i - 1]
        point_before_screen = transformToScreen(point_before)
        pygame.draw.line(window, (0, 0, 255), point_before_screen.to_tuple(), new_point.to_tuple(), 5)
        dis_sum += point_before.distance(p)
    inside_pi=(dis_sum / (2 * RADIOS))
    outside_pi=(outside_sum / (2 * RADIOS))
    esteem_pi= (inside_pi + outside_pi) / 2
    inside_text = font.render(f"Pi is more them = {inside_pi}", True, (200, 0, 0))
    outside_text = font.render(f"Pi is less then = {outside_pi}", True, (200, 0, 0))
    calculate_text = font.render(f"Pi is about ... = {esteem_pi}", True, (200, 0, 0))
    edges_text = font.render(f"The number of vertices : {num_edges}", True, (200, 0, 0))

    window.blit(outside_text, (0, 100))
    window.blit(calculate_text, (0, outside_text.get_height() + 100))
    window.blit(inside_text, (0, calculate_text.get_height() + outside_text.get_height() + 100))
    window.blit(edges_text, (WIDTH - edges_text.get_width() - 100, 100))

    pygame.display.flip()
