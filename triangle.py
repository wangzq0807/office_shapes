import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cairo

class Triangle:
    def __init__(self):
        self.width  = 100
        self.height = 100
        self.pos    = [50, 50]
        self.color  = [0.1, 0.2, 0.5]

    def on_draw(self, ctx):
        ctx.save()
        ctx.set_source_rgb(self.color[0], self.color[1], self.color[2])
        ctx.translate(self.pos[0], self.pos[1])

        ctx.new_path()
        ctx.move_to(self.width/2, 0)
        ctx.line_to(self.width, self.height)
        ctx.line_to(0, self.height)
        ctx.close_path()

        ctx.fill()
        ctx.restore()

    def set_pos(self,newpos):
        self.pos = newpos

class Canvas(Gtk.DrawingArea):
    def __init__(self):
        super(Canvas,self).__init__()
        self.shape = Triangle()

    def on_draw(self, da, ctx):
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)

        self.shape.on_draw(ctx)

if __name__ == '__main__':
    mainwin = Gtk.Window()

    canvas = Canvas()
    canvas.connect('draw', canvas.on_draw)

    mainwin.add(canvas)
    mainwin.show_all()
    Gtk.main()
        