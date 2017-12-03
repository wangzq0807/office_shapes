# -*- coding:utf-8 -*-
import math

class FormulaParser(object):
    def __init__(self, shapedata):
        # self.formula_cache = { }
        self.shape = shapedata # read only
        self.formula_func = { }
        self.init_formula_func()

    def parse(self, key ):
        pass
        # if key in self.test_fmla.keys():
        #     val = self.test_fmla[key]
        #     val_list = val.split(' ')
        #     if val_list[0] in self.formula_func.keys():
        #         func = self.formula_func[val_list[0]]
        #         return func(val_list[1:])
        # else:
        #     ret = int(key)
        #     return ret

    def init_formula_func(self):
        self.formula_func['*/'] = self._mul_div
        self.formula_func['+-'] = self._plus_minus
        self.formula_func['+/'] = self._plus_div
        self.formula_func['ifelse'] = self._if_else
        self.formula_func['?:']   = self._if_else
        self.formula_func['abs']  = self._abs
        self.formula_func['at2']  = self._arctan2
        self.formula_func['cat2'] = self._cos_arctan2
        self.formula_func['cos']  = self._cos
        self.formula_func['max']  = self._max
        self.formula_func['min']  = self._min
        self.formula_func['mod']  = self._mod
        self.formula_func['pin']  = self._pin
        self.formula_func['sat2'] = self._sin_arctan2
        self.formula_func['sin']  = self._sin
        self.formula_func['sqrt'] = self._sqrt
        self.formula_func['tan']  = self._tan
        self.formula_func['val']  = self._val

    def _mul_div(self, values):
        return self.parse(values[0]) * self.parse(values[1]) / self.parse(values[2])

    def _plus_minus(self, values):
        return self.parse(values[0]) + self.parse(values[1]) - self.parse(values[2])

    def _plus_div(self, values):
        return (self.parse(values[0]) + self.parse(values[1])) / self.parse(values[2])
    def _if_else(self, values):
        if self.parse(values[0]):
            return self.parse(values[1])
        else:
            return self.parse(values[2])
    def _abs(self, values):
        return abs(values[0])
    def _arctan2(self, values):
        return math.atan2( self.parse(values[0]), self.parse(values[1]) )
    def _cos_arctan2(self, values):
        return math.cos( self._arctan2(values) )
    def _cos(self, values):
        return math.cos( self.parse(values[0]) )
    def _max(self, values):
        return max(self.parse(values[0]), self.parse(values[1]))
    def _min(self, values):
        return min(self.parse(values[0]), self.parse(values[1]))
    def _mod(self, values):
        return math.sqrt( self.parse(values[0]) * self.parse(values[0])
                        + self.parse(values[1]) * self.parse(values[1])
                        + self.parse(values[2]) * self.parse(values[2]))
    def _pin(self, values):
        if self.parse(values[0]) > self.parse(values[1]):
            return self.parse(values[0])
        elif self.parse(values[1]) > self.parse(values[2]):
            return  self.parse(values[2])
        else:
            return self.parse(values[1])
    def _sin_arctan2(self, values):
        return math.sin( self._arctan2(values) )
    def _sin(self, values):
        return math.sin( self.parse(values[0]) )
    def _sqrt(self, values):
        return math.sqrt( self.parse(values[0]) )
    def _tan(self, values):
        return math.tan( self.parse(values[0]), self.parse(values[1]) )
    def _val(self, values):
        if len(values) == 1:
            return int(values[0])

