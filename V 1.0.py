import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def load_model_data(vertices_file, edges_file, surface_file):
    vertices = []
    edges = []
    surfaces = []

    with open(vertices_file, 'r') as vertices_f:
        for line in vertices_f:
            data = line.split(',')
            vertices.append(tuple(map(float, data)))

    with open(edges_file, 'r') as edges_f:
        for line in edges_f:
            data = line.split(',')
            edges.append(tuple(map(int, data)))

    with open(surface_file, 'r') as surface_f:
        for line in surface_f:
            data = line.split(',')
            surfaces.append(tuple(map(int, data)))

    return vertices, edges, surfaces

def draw_model(vertices, edges, surfaces):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex_index in edge:
            glVertex3fv(vertices[vertex_index])
    glEnd()

    glColor3f(0, 1, 0)  
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex_index in surface:
            glVertex3fv(vertices[vertex_index])
    glEnd()

def main():
    pygame.init()
    display = (700, 400)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(90, (display[0] / display[1]), 0.1, 50)
    glTranslatef(0.0, 0, -5)

    vertices, edges, surfaces = load_model_data('vertices.txt', 'edges.txt', 'surface.txt')

    scale_factor = 0.5  
    glScalef(scale_factor, scale_factor, scale_factor)  

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glRotatef(0.5, 0.25, 0.5, 0.5)  
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_model(vertices, edges, surfaces)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
