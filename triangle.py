#! /usr/bin/python3
# -*- coding:utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
import math

class Triangle:
    def __init__(self):
        self.width  = 100.0
        self.height = 100.0
        self.pos    = [50.0, 50.0]
        self.color  = [0.1, 0.2, 0.5]
        self.rot    = 0.0
        self.tmp    = 0
    
    def _rotate(self, rot):
        pass

    def _set_width(self, w):
        delta  = ( w - self.width ) / 2
        deltaX = delta * math.cos( self.rot )
        deltaY = delta * math.sin( self.rot )
        center = [self.pos[0] + self.width/2, self.pos[1] + self.height/2]
        new_center = [ center[0] + deltaX, center[1] + deltaY ]
        self.width = w
        self.pos[0] = new_center[0] - self.width/2
        self.pos[1] = new_center[1] - self.height/2

    def _set_height(self, h):
        delta  = ( h - self.height ) / 2
        deltaY = delta * math.cos( self.rot )
        deltaX = delta * math.sin( self.rot )
        center = [self.pos[0] + self.width/2, self.pos[1] + self.height/2]
        new_center = [ center[0] - deltaX, center[1] + deltaY ]
        self.height = h
        self.pos[0] = new_center[0] - self.width/2
        self.pos[1] = new_center[1] - self.height/2

    def on_draw(self, ctx):
        self.rot += 0.01
        if self.tmp % 20 < 10:
            self.tmp += 1
            self._set_height(self.height+10)
        else:
            self.tmp += 1
            self._set_height(self.height-10)
        ctx.save()
        ctx.set_source_rgb(self.color[0], self.color[1], self.color[2])
        center = [ self.pos[0]+self.width/2, self.pos[1]+self.height/2]
        ctx.translate(center[0], center[1])
        ctx.rotate(self.rot)

        ctx.new_path()
        ctx.move_to(0, -self.height/2)
        ctx.line_to(-self.width/2, self.height/2)
        ctx.line_to(self.width/2, self.height/2)
        ctx.close_path()

        ctx.fill()
        ctx.restore()

    def set_pos(self, cursor):
        self.pos[0] = cursor[0] - self.width/2
        self.pos[1] = cursor[1] - self.height/2

    def hit_test(self, x, y):
        if x > self.pos[0] and x < (self.pos[0]+self.width):
            if y > self.pos[1] and y < (self.pos[1]+self.height):
                return True

class Canvas(Gtk.DrawingArea):
    def __init__(self):
        super(Canvas,self).__init__()
        self.shape = Triangle()
        self.drag = False

    def on_draw(self, widget, ctx):
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        self.shape.on_draw(ctx)
    
    def on_button_press(self, widget, event):
        if event.button == 1:
            if(self.shape.hit_test(event.x, event.y)):
                self.drag = True
    
    def on_button_release(self, widget, event):
        self.drag = False
    
    def on_mouse_move(self, widget, event):
        if self.drag:
            self.shape.set_pos([event.x, event.y])
            self.queue_draw()

if __name__ == '__main__':
    mainwin = Gtk.Window()

    canvas = Canvas()
    canvas.connect('draw', canvas.on_draw)
    canvas.set_can_focus(True);
    canvas.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                      Gdk.EventMask.BUTTON_RELEASE_MASK |
                      Gdk.EventMask.POINTER_MOTION_MASK )
    canvas.connect('button-press-event', canvas.on_button_press)
    canvas.connect('button-release-event', canvas.on_button_release)
    canvas.connect('motion-notify-event', canvas.on_mouse_move)

    mainwin.add(canvas)
    mainwin.show_all()
    Gtk.main()
        