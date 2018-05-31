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
import pygame

pygame.init()

display_width = 1280 
display_height = 720 

black = (0, 0, 0)
white = (255, 255, 255)
red = (237, 41, 57)

LEFT = 1
RIGHT = 3

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Visibility Graph Simulator')
clock = pygame.time.Clock()

def draw_polygon(polygon, complete=True):
    if complete:
        polygon.append(polygon[0])
    p1 = polygon[0]
    for p2 in polygon[1:]:
        pygame.draw.line(gameDisplay, black, (p1.x, p1.y), (p2.x, p2.y), 4)
        p1 = p2

def draw_visible_vertices(edges):
    for edge in edges:
        pygame.draw.line(gameDisplay, red, (edge.p1.x, edge.p1.y), (edge.p2.x, edge.p2.y), 1)

def game_loop():
    gameExit = False

    polygons = []
    work_polygon = []

    g = vg.VisGraph()
    built = False
    show_static_visgraph = True

    while not gameExit:

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_g:
                    show_static_visgraph = not show_static_visgraph

            if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                pos = pygame.mouse.get_pos()
                work_polygon.append(vg.Point(pos[0], pos[1]))
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT:
                if len(work_polygon) > 1:
                    polygons.append(work_polygon)
                    work_polygon = []
                    g.build(polygons)
                    built = True

        # Display loop 
        gameDisplay.fill(white)

        if len(work_polygon) > 1:
            draw_polygon(work_polygon, complete=False)

        if len(polygons) > 0:
            for polygon in polygons:
                draw_polygon(polygon)

        if built and show_static_visgraph:
            draw_visible_vertices(g.visgraph.get_edges())

        # Logic loop 


        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
    pygame.quit()
    quit()
















