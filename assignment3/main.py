import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

from lib.window import Window
from lib.light import Light
from lib.mode import Mode
from lib.obj import OBJ

class HOS(Window):
    angle = type('angle', (), {
        'angle': 0,
        'height': 0,
    })

    def __init__(self, width, height, name):
        super().__init__(width, height, name)
        self.cam = HOS.angle()
        # objects, In this case, only one object willl be rendered
        self.objects = list()
        # enable lights, see also lib.light
        self.lights = [Light({
                'pos':      (1., 0., 0., 0.),
                'ambient':  (.1, 0., 0., 1.),
                'diffuse':  (1., 0., 0., 1.),
                'specular': (1., 0., 0., 1.),
            }), Light({
                'pos':      (0., 0., 1., 0.),
                'ambient':  (0., 0., .1, 1.),
                'diffuse':  (0., 0., 1., 1.),
                'specular': (0., 0., 1., 1.),
            }), Light({
                'pos':      (0., 1., 0., 0.),
                'ambient':  (0., .1, 0., 1.),
                'diffuse':  (0., 1., 0., 1.),
                'specular': (0., 1., 0., 1.),
            })
        ]

        self.polygonMode = Mode([GL_LINE, GL_FILL])

    def frame(self):
        glBegin(GL_LINES)
        glColor3ub(255,0,0)
        glVertex3fv(np.array([0.,0.,0.]))
        glVertex3fv(np.array([1.,0.,0.]))
        glColor3ub(0,255,0)
        glVertex3fv(np.array([0.,0.,0.]))
        glVertex3fv(np.array([0.,1.,0.]))
        glColor3ub(0,0,255)
        glVertex3fv(np.array([0.,0.,0]))
        glVertex3fv(np.array([0.,0.,1.]))
        glEnd()

    def render(self):
        def cube():
            glBegin(GL_TRIANGLES)

            glNormal3f(0,1,0)
            glVertex3f(0.5,0.5,-0.5)
            glVertex3f(-0.5,0.5,-0.5)
            glVertex3f(-0.5,0.5,0.5)

            glVertex3f(0.5,0.5,-0.5)
            glVertex3f(-0.5,0.5,0.5)
            glVertex3f(0.5,0.5,0.5)

            glNormal3f(0,-1,0)
            glVertex3f(0.5,-0.5,0.5)
            glVertex3f(-0.5,-0.5,0.5)
            glVertex3f(-0.5,-0.5,-0.5)

            glVertex3f(0.5,-0.5,0.5)
            glVertex3f(-0.5,-0.5,-0.5)
            glVertex3f(0.5,-0.5,-0.5)

            glNormal3f(0,0,1)
            glVertex3f(0.5,0.5,0.5)
            glVertex3f(-0.5,0.5,0.5)
            glVertex3f(-0.5,-0.5,0.5)

            glVertex3f(0.5,0.5,0.5)
            glVertex3f(-0.5,-0.5,0.5)
            glVertex3f(0.5,-0.5,0.5)

            glNormal3f(0,0,-1)
            glVertex3f(0.5,-0.5,-0.5)
            glVertex3f(-0.5,-0.5,-0.5)
            glVertex3f(-0.5,0.5,-0.5)

            glVertex3f(0.5,-0.5,-0.5)
            glVertex3f(-0.5,0.5,-0.5)
            glVertex3f(0.5,0.5,-0.5)

            glNormal3f(-1,0,0)
            glVertex3f(-0.5,0.5,0.5)
            glVertex3f(-0.5,0.5,-0.5)
            glVertex3f(-0.5,-0.5,-0.5)

            glVertex3f(-0.5,0.5,0.5)
            glVertex3f(-0.5,-0.5,-0.5)
            glVertex3f(-0.5,-0.5,0.5)

            glNormal3f(1,0,0)
            glVertex3f(0.5,0.5,-0.5)
            glVertex3f(0.5,0.5,0.5)
            glVertex3f(0.5,-0.5,0.5)

            glVertex3f(0.5,0.5,-0.5)
            glVertex3f(0.5,-0.5,0.5)
            glVertex3f(0.5,-0.5,-0.5)
            glEnd()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION) 
        glLoadIdentity()
        gluPerspective(45, 1, 1, 10)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        gluLookAt(5 * np.sin(self.cam.angle),
                  self.cam.height,
                  5 * np.cos(self.cam.angle), 0, 0, 0, 0, 1, 0)
      
        self.frame()

        Light.render()

        glPushMatrix()
        # cube()
        for obj in self.objects:
            obj.render()

        glPopMatrix()

        glDisable(GL_LIGHTING)

    def append(self, obj):
        assert isinstance(obj, OBJ)
        self.objects = [obj]

    def _callback_key(self, window, key, scancode, action, mods):
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_1:
                self.cam.angle += np.radians(-10)
            elif key == glfw.KEY_3:
                self.cam.angle += np.radians(10)
            elif key == glfw.KEY_2:
                self.cam.height += .1
            elif key == glfw.KEY_W:
                self.cam.height += -.1
            elif key == glfw.KEY_A:
                pass # TODO: Zoom in
            elif key == glfw.KEY_S:
                pass # TODO: Zoom out
            elif key == glfw.KEY_Z:
                glPolygonMode(GL_FRONT_AND_BACK, self.polygonMode.get(next=True))

    def _callback_drop(self, window, paths):
        path = paths[0]
        if len(paths) > 1:
            print ('Only one obj file can be attached at a time')
        obj = OBJ.read_obj(path)
        # print object information to stdout
        print (obj)
        self.append(obj)


def main():
    if not glfw.init(): return
    window = HOS(640, 640, '2015004584')
    if not window.context:
        glfw.terminate()
        return

    glfw.make_context_current(window.context)

    glfw.set_key_callback(window.context, window._callback_key)
    glfw.set_drop_callback(window.context, window._callback_drop)

    glfw.swap_interval(1)

    while not glfw.window_should_close(window.context):
        glfw.poll_events()
        window.render()
        glfw.swap_buffers(window.context)

    glfw.terminate()

if __name__ == "__main__":
    main()
