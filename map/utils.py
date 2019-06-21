import plotly.graph_objs as go
import csv
import pandas as pd


def town():
    df = pd.read_csv('map/csv/city_rus.csv')
    df.head()
    df['text'] = df['name'] + '<br>Население ' + (df['pop'] / 1e3).astype(str) + ' тыс'
    limits = [(0, 1e4), (1e4+1, 1e5), (1e5+1, 5e5), (5e5+1, 1e6), (1e6+1, 1e8)]
    colors = ["blue", "green", "yellow", "orange", "red"]
    size = [10, 15, 20, 25, 30]
    cities = []
    scale = 80000
    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[df['pop']>=lim[0]][df['pop']<=lim[1]]
        city = go.Scattergeo(
            locationmode='ISO-3',
            lon=df_sub['lon'],
            lat=df_sub['lat'],
            text=df_sub['text'],
            marker=go.scattergeo.Marker(
                size=size[i],
                color=colors[i],
                line=go.scattergeo.marker.Line(
                    width=0.5, color='rgb(40,40,40)'
                ),
                sizemode='diameter'
            ),
            name='{0} - {1}'.format(lim[0], lim[1]))
        cities.append(city)

    layout = go.Layout(
        title=go.layout.Title(
            text='Население'
        ),
        showlegend=True,
        autosize=False,
        width=1500, height=1000,
        margin=dict(l=50, r=50, b=50, t=50, pad=4, autoexpand=True),
        geo=go.layout.Geo(
            scope='world',
            showland=True,
            landcolor='rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)",
            showrivers=True,
            projection=dict(type='mercator'),

        )
    )

    return go.Figure(data=cities, layout=layout)
