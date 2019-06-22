import csv
import scipy as sp
import plotly.graph_objs as go
import random
import datetime


def mnkGP1(x, y):
    d = 2 # степень полинома
    fp, residuals, rank, sv, rcond = sp.polyfit(x, y, d, full=True) # Модель
    f = sp.poly1d(fp) # аппроксимирующая функция
    print('Коэффициент -- a %s  '%round(fp[0],4))
    print('Коэффициент-- b %s  '%round(fp[1],4))
    print('Коэффициент -- c %s  '%round(fp[2],4))
    y1 = [fp[0]*x[i]**2+fp[1]*x[i]+fp[2] for i in range(0,len(x))] # значения функции a*x**2+b*x+c
    so = round(sum([abs(y[i]-y1[i]) for i in range(0, len(x))])/(len(x)*sum(y))*100, 4) # средняя ошибка
    print('Average quadratic deviation '+str(so))
    fx = sp.linspace(x[0], x[-1]*1.2 + 1, len(x)) # можно установить вместо len(x) большее число для интерполяции
    """
    plt.title(axe['title'],size=14)
    plt.xlabel(axe['x'], size=14)
    plt.ylabel(axe['y'], size=14)
    plt.plot(x, y, 'o', label='Оригинал', markersize=10)
    plt.plot(fx, f(fx), label='Функция', linewidth=2)
    plt.legend(loc='best')
    plt.grid(True)
    plt.savefig(axe['file_name'])
    plt.close()
    """
    x2 = x + [x[-1]+i for i in range(365)]
    return x2, f(x2)


def big_graph():
    x1 = list()
    y1 = list()
    with open('_csv/speed.txt') as csvfile:
        for line in csv.reader(csvfile, delimiter=';'):
            x1.append(line[0])
            y1.append(float(line[2]))
    x1 = date_to_int(x1)
    # Полученны реальные результаты измерений, делаю график для них
    trace0 = go.Scatter(
        x=int_to_date(x1),
        y=y1,
        mode='markers',
        name="Доход",
        hovertemplate='Реальных доход: %{y} руб',
        marker=dict(
            size=15,
            color='#2ECCFA',
            line=dict(
                width=2,
                color='black'
            )
        )
    )

    x2, y2 = mnkGP1(x1, y1)
    trace1 = go.Scatter(
        x=int_to_date(x2),
        y=y2,
        mode='lines',
        name="Прогноз",
        hovertemplate='Прогноз дохода: %{y} руб',
        marker=dict(
            size=15,
            color='RED',
            line=dict(
                width=2,
                color='black'
            )
        )
    )
    # print('x2=', x2)
    layout = {
        "title": "Пример апроксимации",
        "grid": {"rows": 1, "columns": 1},
    }
    return go.Figure(data=[trace0, trace1], layout=layout)


def date_to_int(vector):
    out = list()
    for i in vector:
        # Дней с 1-го года
        out.append(datetime.datetime.strptime(i, "%d.%m.%Y").toordinal())
    # print('out=', out)
    return out


def int_to_date(vector):
    out = list()
    for i in vector:
        out.append(datetime.datetime.fromordinal(i))
    return out
