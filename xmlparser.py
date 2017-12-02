#! /usr/bin/python3
# -*- coding:utf-8 -*-
import xml
from xml import sax
from xml.parsers.expat import ParserCreate

class XmlHandler(object):
    def __init__(self):
        pass
    def startElement(self, name, attrs):
        pass
    def endElement(self, name):
        pass
    def characters(self, content):
        pass

class PathMoveToHandler(XmlHandler):
    def __init__(self):
        pass

class PathHandler(XmlHandler):
    def __init__(self):
        self.cur_handler = None

    def startElement(self, name, attrs):
        if name == 'path':
            pass
        elif name == 'moveTo':
            self.cur_handler = PathMoveToHandler()
        elif self.cur_handler is not None:
            self.cur_handler.startElement(name, attrs)

    def endElement(self, name):
        if name == 'path':
            pass

    def characters(self, content):
        pass

class GuidListHandler(XmlHandler):
    def __init__(self, guid_dict):
        self.guid_dict = guid_dict

    def startElement(self, name, attrs):
        if name == 'gd':
            name = attrs.get('name')
            fmla = attrs.get('fmla')
            self.guid_dict[name] = fmla

    def endElement(self, name):
        pass

    def characters(self, content):
        pass

class OOXMLShape():
    def __init__(self, name):
        self.guid_dict = {}
        self.adjguid_dict = {}
        self.path_list = []
        self.cur_handler = None
    def startElement(self, name, attrs):
        if name == 'avLst':     # adjustment
            self.cur_handler = GuidListHandler(self.adjguid_dict)
        elif name == 'gdLst':   # fmla
            self.cur_handler = GuidListHandler(self.guid_dict)
        elif name == 'ahLst':   # control point
            pass
        elif name == 'cxnLst':  # vertex
            pass
        elif name == 'rect':    # text rect
            pass
        elif name == 'pathLst': # path
            pass
        elif self.cur_handler is not None:
            self.cur_handler.startElement(name, attrs)

    def endElement(self, name):
        pass
    def characters(self, content):
        pass

class XmlRootHandler(xml.sax.ContentHandler):
    def __init__(self):
        super(XmlRootHandler, self).__init__()
        self.level = 0
        self.shape_list = {}
        self.cur_handler = None

    def startElement(self, name, attrs):
        self.level += 1
        if self.level == 2:
            if name == 'quadArrow':
                print(name)
            shape = OOXMLShape(name)
            self.shape_list[name] = shape
            self.cur_handler = shape
        elif self.level > 2 and self.cur_handler is not None:
            self.cur_handler.startElement(name, attrs)

    def endElement(self, name):
        if self.level > 2 and self.cur_handler is not None:
            self.cur_handler.endElement(name)
        elif self.level == 2 and self.cur_handler is not None:
            pass
        self.level -= 1

    def characters(self, content):
        pass

if __name__ == '__main__':
    handler = XmlRootHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler( handler )
    parser.parse('presetShapeDefinitions.xml')
    pass