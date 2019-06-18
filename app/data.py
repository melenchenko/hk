from plotly.offline import plot
import plotly.graph_objs as go


def scatterplot(datas, schema):
    data = []
    for key, value in datas.items():
        x_ = []
        y_ = []
        for field in value:
            x_.append(getattr(field, schema['x']))
            y_.append(getattr(field, schema['y']))

        data.append(go.Scatter(
            x=x_,
            y=y_,
            name=key,
            mode='markers',
            marker=dict(
                size=10,
                color=schema['targets'][key]['color'],
                line=dict(
                    width=2,
                )
            )
        ))

    layout = dict(
        title='Styled Scatter',
        yaxis=dict(zeroline=False),
        xaxis=dict(zeroline=False)
    )

    fig = dict(data=data, layout=layout)
    return plot(fig, output_type='div', include_plotlyjs=True)
