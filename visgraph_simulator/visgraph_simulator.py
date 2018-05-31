"""
The MIT License (MIT)

Copyright (c) 2016 Christian August Reksten-Monsen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import pyvisgraph as vg
from pyvisgraph.visible_vertices import visible_vertices
import pygame

pygame.init()

display_width = 1280 
display_height = 720 

black = (0, 0, 0)
white = (255, 255, 255)
red = (237, 41, 57)
gray = (169, 169, 169)
green = (0, 128, 0)

LEFT = 1
RIGHT = 3

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Visibility Graph Simulator')
clock = pygame.time.Clock()

def draw_polygon(polygon, color, size, complete=True):
    if complete:
        polygon.append(polygon[0])
    p1 = polygon[0]
    for p2 in polygon[1:]:
        pygame.draw.line(gameDisplay, color, (p1.x, p1.y), (p2.x, p2.y), size)
        p1 = p2

def draw_visible_vertices(edges, color, size):
    for edge in edges:
        pygame.draw.line(gameDisplay, color, (edge.p1.x, edge.p1.y), (edge.p2.x, edge.p2.y), size)

def draw_visible_mouse_vertices(pos, points, color, size):
    for point in points:
        pygame.draw.line(gameDisplay, color, (pos.x, pos.y), (point.x, point.y), size)

def draw_mode(mode_txt):
    font = pygame.font.SysFont(None, 25)
    text = font.render(mode_txt, True, black)
    gameDisplay.blit(text, (0, 0))

def game_loop():
    gameExit = False

    polygons = []
    work_polygon = []
    mouse_point = None
    mouse_vertices = []
    start_point = None
    end_point = None
    shortest_path = []

    g = vg.VisGraph()
    built = False
    show_static_visgraph = True
    show_mouse_visgraph = True
    mode_draw = True
    mode_path = False

    while not gameExit:

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_g:
                    show_static_visgraph = not show_static_visgraph
                if event.key == pygame.K_m:
                    show_mouse_visgraph = not show_mouse_visgraph
                if event.key == pygame.K_d:
                    mode_draw = not mode_draw
                    mode_path = False
                    shortest_path = [] 
                    start_point = []
                    end_point = []
                if event.key == pygame.K_s:
                    if mode_path:
                        shortest_path = []
                        start_point = []
                        end_point = []
                    mode_path = not mode_path
                    mode_draw = False

            if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                pos = pygame.mouse.get_pos()
                if mode_draw:
                    work_polygon.append(vg.Point(pos[0], pos[1]))
                elif mode_path and built:
                    start_point = vg.Point(pos[0], pos[1])
                    if end_point:
                        shortest_path = g.shortest_path(start_point, end_point)
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT:
                pos = pygame.mouse.get_pos()
                if mode_draw:
                    if len(work_polygon) > 1:
                        polygons.append(work_polygon)
                        work_polygon = []
                        g.build(polygons)
                        built = True
                elif mode_path and built:
                    end_point = vg.Point(pos[0], pos[1])
                    if start_point:
                        shortest_path = g.shortest_path(start_point, end_point)

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if built and show_mouse_visgraph:
                    mouse_point = vg.Point(pos[0], pos[1])
                    mouse_vertices = visible_vertices(mouse_point, g.graph)
                if mode_path and built and pygame.mouse.get_pressed()[LEFT-1]: 
                    start_point = vg.Point(pos[0], pos[1])
                    if end_point:
                        shortest_path = g.shortest_path(start_point, end_point)
                if mode_path and built and pygame.mouse.get_pressed()[RIGHT-1]: 
                    end_point = vg.Point(pos[0], pos[1])
                    if start_point:
                        shortest_path = g.shortest_path(start_point, end_point)

        # Display loop 
        gameDisplay.fill(white)

        if len(work_polygon) > 1:
            draw_polygon(work_polygon, black, 3, complete=False)

        if len(polygons) > 0:
            for polygon in polygons:
                draw_polygon(polygon, black, 3)

        if built and show_static_visgraph:
            draw_visible_vertices(g.visgraph.get_edges(), gray, 1)

        if built and show_mouse_visgraph and len(mouse_vertices) > 0:
            draw_visible_mouse_vertices(mouse_point, mouse_vertices, gray, 1)

        if len(shortest_path) > 1:
            draw_polygon(shortest_path, red, 3, complete=False)

        if mode_draw:
            draw_mode("-- DRAW MODE --")
        elif mode_path:
            draw_mode("-- SHORTEST PATH MODE --")
        else:
            draw_mode("-- VIEW MODE --")

        # Logic loop 

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
    pygame.quit()
    quit()
















