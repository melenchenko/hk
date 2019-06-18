from django.utils.safestring import mark_safe
from django.template import Library

import json


register = Library()

@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))


COLORS_CONST = ('#FF00BF', '#F4FA58', '#2EFE2E', '#81F7F3', '#FA8258', '#0040FF')


class Card:
    """Класс для представления данных в элементе Card dashboard"""

    def __init__(self, name, value, trend=None, success=True):
        self.name = name
        self.value = value
        self.trend = trend
        self.success = success

    def to_dict(self):
        if self.success:
            span = 'text-success bg-success-light'
            div = 'text-success'
        else:
            div = 'text-danger'
            span = 'text-danger bg-danger-light'

        if self.trend > 0:
            arrow = 'fa-arrow-up'
        elif self.trend < 0:
            arrow = 'fa-arrow-down'
        else:
            arrow = ""
        return {'name': self.name, 'value': self.value, 'trend': f"{self.trend}%", 'span': span, 'div': div, 'arrow': arrow}


class Graph:
    """Класс для представления графиков"""

    def __init__(self, name, style, data=None):
        self.name = name
        self.style = style
        self.data = data

    def to_dict(self):
        return {'name': self.name, 'style': self.style, 'data': self.data}


class Chart:
    """Класс для представления Chart"""

    def __init__(self, name, lines):
        self.name = name
        # (("Мужчины", 10),)
        self.lines = lines

    def to_dict(self):
        colors = dict()
        j = 0
        for i in self.lines:
            colors[i[0]] = COLORS_CONST[j]
            j += 1
            if j >= len(COLORS_CONST):
                j = 0
        return {'name': self.name, 'columns': js(self.lines), 'colors': js(colors)}


class Histogram:
    """Класс для представления гистограмм"""

    def __init__(self, name, label, series=None):
        self.name = name
        self.label = label
        self.series = series

    def to_dict(self):
        return {'name': self.name, 'labels': js(self.label), 'data': js(self.series)}

