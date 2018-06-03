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

def draw_text(mode_txt, color, size, x, y):
    font = pygame.font.SysFont(None, size)
    text = font.render(mode_txt, True, color)
    gameDisplay.blit(text, (x, y))

def help_screen():
    rectw = 550
    recth = 500
    rectwi = rectw-10
    recthi = recth-10
    startx = display_width*0.5-rectw/2
    starty = display_height*0.5-recth/2
    startxi = display_width*0.5-rectwi/2
    startyi = display_height*0.5-recthi/2

    helping = True
    while helping:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_h:
                    helping = False

        pygame.draw.rect(gameDisplay, black, (startx, starty, rectw, recth))
        pygame.draw.rect(gameDisplay, white, (startxi, startyi, rectwi, recthi))

        draw_text("-- VISIBILITY GRAPH SIMULATOR --", black, 30, startxi+90, startyi+10)
        draw_text("Q - QUIT", black, 25, startxi+10, startyi+45)
        draw_text("H - TOGGLE HELP SCREEN (THIS SCREEN)", black, 25, startxi+10, startyi+80)
        draw_text("D - TOGGLE DRAW MODE", black, 25, startxi+10, startyi+115)
        draw_text("    Draw polygons by left clicking to set a point of the", black, 25, startxi+10, startyi+150)
        draw_text("    polygon. Right click to close and finish the polygon.", black, 25, startxi+10, startyi+180)
        draw_text("    U - UNDO LAST POLYGON POINT PLACEMENT", black, 25, startxi+10, startyi+215)
        draw_text("    C - CLEAR THE SCREEN", black, 25, startxi+10, startyi+250)
        draw_text("S - TOGGLE SHORTEST PATH MODE", black, 25, startxi+10, startyi+285)
        draw_text("    Left click to set start point, right click to set end point.", black, 25, startxi+10, startyi+320)
        draw_text("    Hold left/right mouse button down to drag start/end point.", black, 25, startxi+10, startyi+355)
        draw_text("M - TOGGLE VISIBILE VERTICES FROM MOUSE CURSOR", black, 25, startxi+10, startyi+390)
        draw_text("G - TOGGLE POLYGON VISIBILITY GRAPH", black, 25, startxi+10, startyi+425)
        draw_text("© Christian August Reksten-Monsen", black, 20, startxi+140, startyi+470)

        pygame.display.update()
        clock.tick(10)

class Simulator():

    def __init__(self):
        self.polygons = []
        self.work_polygon = []
        self.mouse_point = None
        self.mouse_vertices = []
        self.start_point = None
        self.end_point = None
        self.shortest_path = []

        self.g = vg.VisGraph()
        self.built = False
        self.show_static_visgraph = True
        self.show_mouse_visgraph = False
        self.mode_draw = True
        self.mode_path = False

    def toggle_draw_mode(self):
        self.mode_draw = not self.mode_draw
        self._clear_shortest_path()
        self.mode_path = False

    def close_polygon(self):
        if len(self.work_polygon) > 1:
            self.polygons.append(self.work_polygon)
            self.work_polygon = []
            self.g.build(self.polygons, status=False)
            self.built = True

    def draw_point_undo(self):
        if len(self.work_polygon) > 0:
            self.work_polygon.pop()

    def toggle_shortest_path_mode(self):
        if self.mode_path:
            self._clear_shortest_path()
        self.mode_path = not self.mode_path
        self.mode_draw = False

    def clear_all(self):
        self.__init__()

    def _clear_shortest_path(self):
        self.shortest_path = []
        self.start_point = []
        self.end_point = [] 

def game_loop():
    sim = Simulator()
    gameExit = False

    while not gameExit:

        # Event loop
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_h:
                    help_screen()
                elif event.key == pygame.K_g:
                    sim.show_static_visgraph = not sim.show_static_visgraph
                elif event.key == pygame.K_m:
                    sim.show_mouse_visgraph = not sim.show_mouse_visgraph
                elif event.key == pygame.K_d:
                    sim.toggle_draw_mode()
                elif event.key == pygame.K_s:
                    sim.toggle_shortest_path_mode()

            if sim.mode_draw:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_u:
                        sim.draw_point_undo()
                    elif event.key == pygame.K_c:
                        sim.clear_all()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == LEFT:
                        sim.work_polygon.append(vg.Point(pos[0], pos[1]))
                    elif event.button == RIGHT:
                        sim.close_polygon()

            if sim.mode_path and sim.built:
                if event.type == pygame.MOUSEBUTTONUP or any(pygame.mouse.get_pressed()):
                    if pygame.mouse.get_pressed()[LEFT-1] or event.button == LEFT:
                        sim.start_point = vg.Point(pos[0], pos[1])
                    elif pygame.mouse.get_pressed()[RIGHT-1] or event.button == RIGHT:
                        sim.end_point = vg.Point(pos[0], pos[1])
                    if sim.start_point and sim.end_point:
                        sim.shortest_path = sim.g.shortest_path(sim.start_point, sim.end_point)

            if sim.show_mouse_visgraph and sim.built:
                if event.type == pygame.MOUSEMOTION:
                    sim.mouse_point = vg.Point(pos[0], pos[1])
                    sim.mouse_vertices = sim.g.find_visible(sim.mouse_point)

        # Display loop
        gameDisplay.fill(white)

        if len(sim.work_polygon) > 1:
            draw_polygon(sim.work_polygon, black, 3, complete=False)

        if len(sim.polygons) > 0:
            for polygon in sim.polygons:
                draw_polygon(polygon, black, 3)

        if sim.built and sim.show_static_visgraph:
            draw_visible_vertices(sim.g.visgraph.get_edges(), gray, 1)

        if sim.built and sim.show_mouse_visgraph and len(sim.mouse_vertices) > 0:
            draw_visible_mouse_vertices(sim.mouse_point, sim.mouse_vertices, gray, 1)

        if len(sim.shortest_path) > 1:
            draw_polygon(sim.shortest_path, red, 3, complete=False)

        if sim.mode_draw:
            draw_text("-- DRAW MODE --", black, 25, 5, 5)
        elif sim.mode_path:
            draw_text("-- SHORTEST PATH MODE --", black, 25, 5, 5)
        else:
            draw_text("-- VIEW MODE --", black, 25, 5, 5)

        pygame.display.update()
        clock.tick(20)

if __name__ == "__main__":
    gameDisplay.fill(white)
    help_screen()
    game_loop()
    pygame.quit()
    quit()
