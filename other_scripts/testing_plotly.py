import plotly.offline as py
import plotly.graph_objs as go
import plotly
plotly.tools.set_credentials_file(username='cjuliankopp', api_key='hjnIV1XMAONzNbPdWHyQ')
import numpy as np

data = go.Data([
    go.Mesh3d(
        x=[32, 32, 32, 32, 32, 16, 16, 16, 16, 16, 8, 8, 8, 8, 8],
        y=[60, 180, 360, 540, 660, 60, 180, 360, 540, 660, 60, 180, 360, 540, 660],
        z=[6.08569199, 3.79651954, 3.14880474, 2.96244272, 2.89275642, 5.09032082, 2.78085133, 1.87804022, 1.53846753,
           1.38509935, 3.99771527, 2.51647348, 1.74689732, 1.42497564, 1.26372289],
        colorbar = go.ColorBar(
            title='z'
        ),
        colorscale = [['6', 'rgb(255, 0, 0)'],
                      ['3', 'rgb(0, 255, 0)'],
                      ['0', 'rgb(0, 0, 255)']],
        intensity = [0,  6],
        name = 'y',
        showscale = True
    )
])
layout = go.Layout(
                    scene = dict(
                    xaxis = dict(
                        title = 'map-size',
                        tickmode = 'array',
                        ticktext= ['8','16','32'],
                        tickvals=[8, 16, 32]
                    ),
                    yaxis = dict(
                        title='interval-size',
                        ticktext= ['1','3','6','9','11'],
                        tickvals= [60,180,360,540,660]
                    ),
                    zaxis = dict(
                        nticks=4, ticks='outside',
                        tick0=0, tickwidth=4),),
                    width=700,
                    margin=dict(
                    r=10, l=10,
                    b=10, t=10)
                  )
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='3d-mesh-tetrahedron-python')


# data = go.Data([
#     go.Mesh3d(
#         x=[32, 32, 32, 32, 32, 16, 16, 16, 16, 16, 8, 8, 8, 8, 8],
#                 y=[60, 180, 360, 540, 660, 60, 180, 360, 540, 660, 60, 180, 360, 540, 660],
#                 z=[6.08569199, 3.79651954, 3.14880474, 2.96244272, 2.89275642, 5.09032082, 2.78085133, 1.87804022, 1.53846753,
#                    1.38509935, 3.99771527, 2.51647348, 1.74689732, 1.42497564, 1.26372289],
#         colorbar = go.ColorBar(
#             title='z'
#         ),
#         colorscale = [['0', 'rgb(255, 0, 0)'],
#                       ['0.5', 'rgb(0, 255, 0)'],
#                       ['1', 'rgb(0, 0, 255)']],
#        intensity = [0, 0.33, 0.66, 1],
#         i = [0, 0, 0, 1],
#         j = [1, 2, 3, 2],
#         k = [2, 3, 1, 3],
#         name = 'y',
#         showscale = True
#     )
# ])
# layout = go.Layout(
#                     scene = dict(
#                     xaxis = dict(
#                         title = 'map-size',
#                         tickmode = 'array',
#                         ticktext= ['8','16','32'],
#                         tickvals=[8, 16, 32]
#                     ),
#                     yaxis = dict(
#                         title='interval-size',
#                         ticktext= ['1','3','6','9','11'],
#                         tickvals= [60,180,360,540,660]
#                     ),
#                     zaxis = dict(
#                         nticks=4, ticks='outside',
#                         tick0=0, tickwidth=4),),
#                     width=700,
#                     margin=dict(
#                     r=10, l=10,
#                     b=10, t=10)
#                   )
# fig = go.Figure(data=data, layout=layout)
# py.plot(fig, filename='3d-mesh-tetrahedron-python')