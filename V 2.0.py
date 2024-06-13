import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def load_model_data(vertices_file, edges_file):
    vertices = []
    edges = []
    
    with open(vertices_file, 'r') as vertices_f:
        for line in vertices_f:
            data = line.split(',')
            vertices.append(tuple(map(float, data)))
    
    with open(edges_file, 'r') as edges_f:
        for line in edges_f:
            data = line.split(',')
            edges.append(tuple(map(int, data)))
    
    return vertices, edges

def draw_model(vertices, edges):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex_index in edge:
            glVertex3fv(vertices[vertex_index])
    glEnd()

def draw_axes():
    glBegin(GL_LINES)
    
    # X-axis (Red)
    glColor3f(1, 0, 0)
    glVertex3f(-5, 0, 0)
    glVertex3f(5, 0, 0)

    # Y-axis (Green)
    glColor3f(0, 1, 0)
    glVertex3f(0, -5, 0)
    glVertex3f(0, 5, 0)

    # Z-axis (Blue)
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, -5)
    glVertex3f(0, 0, 5)

    glEnd()

def main():
    pygame.init()
    display = (700, 400)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(90, (display[0] / display[1]), 0.1, 50)
    glTranslatef(0.0, 0, -10)

    vertices, edges = load_model_data('vertices.txt', 'edges.txt')

    scale_factor = 1.0  
    rotation_angles = {'OX': 0, 'OY': 0, 'OZ': 0, 'All': 0}  

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Керування масштабуванням
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    scale_factor += 0.1
                elif event.key == pygame.K_DOWN:
                    scale_factor -= 0.1

            # Керування обертанням за допомогою миші
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ - обертання навколо OX
                    rotation_angles['OX'] += 5
                elif event.button == 3:  # ПКМ - обертання навколо OY
                    rotation_angles['OY'] += 5
                elif event.button == 2:  # СКМ - обертання навколо OZ
                    rotation_angles['OZ'] += 5
                elif event.button == 4:  # Колесо миші вгору - обертання всіх одночасно
                    rotation_angles['All'] += 5
                elif event.button == 5:  # Колесо миші вниз - обертання всіх одночасно в протилежному напрямку
                    rotation_angles['All'] -= 5

            # Керування обертанням за допомогою клавіш Ctrl + X, Ctrl + Y та Ctrl + Z
            if event.type == pygame.KEYDOWN and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if event.key == pygame.K_x:  # Обертання навколо осі X
                    rotation_angles['OX'] += 5
                elif event.key == pygame.K_y:  # Обертання навколо осі Y
                    rotation_angles['OY'] += 5
                elif event.key == pygame.K_z:  # Обертання навколо осі Z
                    rotation_angles['OZ'] += 5

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # Масштабування
        glScalef(scale_factor, scale_factor, scale_factor)

        # Відображення координатних вісей
        draw_axes()

        # Обертання по осях OX, OY, OZ та всіх одночасно
        glRotatef(rotation_angles['OX'], 1, 0, 0)  # Ось OX
        glRotatef(rotation_angles['OY'], 0, 1, 0)  # Ось OY
        glRotatef(rotation_angles['OZ'], 0, 0, 1)  # Ось OZ
        glRotatef(rotation_angles['All'], 1, 1, 1)  # Всі одночасно

        draw_model(vertices, edges)

        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
