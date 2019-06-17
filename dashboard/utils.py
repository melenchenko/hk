class Card:
    """Класс для представления данных в элементе Card dashboard"""

    def __init__(self, name, value, trend=None, data=None):
        self.name = name
        self.value = value
        self.trend = trend
        self.data = data

    def to_dict(self):
        return {'name': self.name, 'value': self.value, 'trend': self.trend, 'data': self.data }


class Graph:
    """Класс для представления графиков"""

    def __init__(self, name, style, data=None):
        self.name = name
        self.style = style
        self.data = data

    def to_dict(self):
        return {'name': self.name, 'style': self.style, 'data': self.data}


class Histogram:
    """Класс для представления гистограмм"""

    def __init__(self, name, label, series=None):
        self.name = name
        self.label = label
        self.series = series
