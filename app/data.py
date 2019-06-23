from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
import os.path


def scatterplot(data, schema):
    data_ = []
    for key, value in data.items():
        x_ = []
        y_ = []
        for field in value:
            x_.append(getattr(field, schema['x']))
            y_.append(getattr(field, schema['y']))

        data_.append(go.Scatter(
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

    fig = dict(data=data_, layout=layout)
    return plot(fig, output_type='div', include_plotlyjs=True)


def prepare_data(data, schema):
    x = []
    y = []
    for item in data:
        x_ = []
        for field_name in schema['fields']['vars']:
            attr = getattr(item, field_name)
            if field_name in schema['fields']['decorators']:
                attr = schema['fields']['decorators'][field_name](attr, True)
            x_.append(attr)
        x.append(x_)
        y.append(getattr(item, schema['fields']['target']))
    return np.array(x), np.array(y)


def fit(data, schema, pk=0):
    filename = 'fits.dumps/' + schema['moduleName'] + '_' + schema['modelName'] + str(pk) +  '.pkl'
    if os.path.exists(filename):
        clf = joblib.load(filename)
    else:
        if schema['modelName'] == 'gauss':
            clf = GaussianNB()
        elif schema['modelName'] == 'knn':
            clf = KNeighborsClassifier()
        dataX, dataY = prepare_data(data, schema)
        clf.fit(dataX, dataY)
        joblib.dump(clf, filename)
    return clf


def parse_form(form, schema):
    result = []
    for field_name in schema['fields']['vars']:
        attr = form.cleaned_data[field_name]
        if field_name in schema['fields']['decorators']:
            attr = schema['fields']['decorators'][field_name](attr)
        result.append(attr)
    return [result]
