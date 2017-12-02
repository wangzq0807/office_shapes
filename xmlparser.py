#! /usr/bin/python3
# -*- coding:utf-8 -*-
import xml
from xml import sax
from xml.parsers.expat import ParserCreate

class PathHandler(object):
    def __init__(self):
        self.processing = False
    def startElement(self, name, attrs):
        if name == 'path':
            self.processing = True
        elif name == 'moveTo':
            pass

    def endElement(self, name):
        if name == 'path':
            self.processing = False

    def characters(self, content):
        pass

class GuidListContext(object):
    def __init__(self, guid_list):
        self.guid_list = guid_list

    def startElement(self, name, attrs):
        if name == 'gd':
            name = attrs.get('name')
            fmla = attrs.get('fmla')
            self.guid_list[name] = fmla

    def endElement(self, name):
        pass

    def characters(self, content):
        pass

class OneShape():
    def __init__(self, name):
        self.guid_list = {}
        self.adjguid_list = {}
        self.cur_context = None
    def startElement(self, name, attrs):
        if name == 'avLst':     # adjustment
            self.cur_context = GuidListContext(self.adjguid_list)
        elif name == 'gdLst':   # fmla
            self.cur_context = GuidListContext(self.guid_list)
        elif name == 'ahLst':   # control point
            pass
        elif name == 'cxnLst':  # vertex
            pass
        elif name == 'rect':    # text rect
            pass
        elif name == 'pathLst': # path
            pass
        elif self.cur_context is not None:
            self.cur_context.startElement(name, attrs)

    def endElement(self, name):
        pass
    def characters(self, content):
        pass

class framework(xml.sax.ContentHandler):
    def __init__(self):
        super(framework, self).__init__()
        self.level = 0
        self.shape_list = {}
        self.cur_context = None

    def startElement(self, name, attrs):
        self.level += 1
        if self.level == 2:
            shape = OneShape(name)
            self.shape_list[name] = shape
            self.cur_context = shape
        elif self.level > 2 and self.cur_context is not None:
            self.cur_context.startElement(name, attrs)

    def endElement(self, name):
        if self.level > 2 and self.cur_context is not None:
            self.cur_context.endElement(name)
        self.level -= 1

    def characters(self, content):
        pass

if __name__ == '__main__':
    handler = framework()
    parser = xml.sax.make_parser()
    parser.setContentHandler( handler )
    parser.parse('presetShapeDefinitions.xml')
    pass