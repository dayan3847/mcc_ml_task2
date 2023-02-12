import numpy as np
import plotly.graph_objs as go
from typing import List
from plotly.graph_objs import Figure
from src.models import Artificial
from src.models import Polynomial
from src.tools import GrapherPlotly


class GrapherPlotly2D(GrapherPlotly):

    def __init__(self):
        super().__init__()
        self.figure_2d_data: Figure = go.Figure()
        self.figure_2d_data.update_layout(
            xaxis_title="x0",
            yaxis_title="x1",
            xaxis_range=self.area_to_pot[0],
            yaxis_range=self.area_to_pot[1],
        )
        self.figure_2d_data.add_trace(
            go.Scatter(
                x=[-10, 10],
                y=[0, 0],
                mode='lines',
                name='x',
                marker_color='gray'
            )
        )
        self.figure_2d_data.add_trace(
            go.Scatter(
                x=[0, 0],
                y=[-10, 10],
                mode='lines',
                name='y',
                marker_color='gray',
            )
        )

        self.figure_2d_error: Figure = go.Figure()
        self.figure_2d_error.update_layout(
            xaxis_title="iteration",
            yaxis_title="error",
        )

    def plot_artificial_data_2d(self, artificial: List[Artificial]):
        data_to_print: dict = {}
        for data in artificial:
            if data.y not in data_to_print:
                data_to_print[data.y] = {'x0': [], 'x1': []}
            data_to_print[data.y]['x0'].append(data.x_vector[0])
            data_to_print[data.y]['x1'].append(data.x_vector[1])
        for key in data_to_print:
            color: str = 'purple' if key == 0 else 'orange' if key == 1 else 'gray'
            self.figure_2d_data.add_trace(
                go.Scatter(
                    x=data_to_print[key]['x0'],
                    y=data_to_print[key]['x1'],
                    mode='markers',
                    name=str(key),
                    marker_color=color,
                )
            )

    def plot_polynomial(self, polinomial: Polynomial, name: str, color: str = 'gray'):
        if polinomial.get_variables_count() > 2:
            return
        if polinomial.get_last_variable_degree() > 1:
            return
        x0_list = np.linspace(-3, 3, 100)
        x1_list = []
        for x0 in x0_list:
            x1 = polinomial.evaluate_despejando([x0], 1)
            x1_list.append(x1)
        self.figure_2d_data.add_trace(
            go.Scatter(
                x=x0_list,
                y=x1_list,
                mode='lines',
                name=name,
                marker_color=color,
            )
        )

    def plot_sigmoid_function(self):
        range = (-20, 20)
        x0_list = np.linspace(range[0], range[1], 100)
        x1_list = []
        for x0 in x0_list:
            x1 = 1 / (1 + np.exp(-x0))
            x1_list.append(x1)

        figure_sigmoid: Figure = go.Figure()
        figure_sigmoid.update_layout(
            xaxis_title="x",
            yaxis_title="sigmoid(x)",
            xaxis_range=(range[0], range[1]),
            yaxis_range=(-.1, 1.1),
        )
        figure_sigmoid.add_trace(
            go.Scatter(
                x=x0_list,
                y=x1_list,
                mode='lines',
                name='Sigmoid',
                marker_color='green',
            )
        )
        # add horizontal lines for 0 and 1
        figure_sigmoid.add_trace(
            go.Scatter(
                x=[range[0], range[1]],
                y=[0, 0],
                mode='lines',
                name='0',
                marker_color='gray'
            )
        )
        figure_sigmoid.add_trace(
            go.Scatter(
                x=[range[0], range[1]],
                y=[1, 1],
                mode='lines',
                name='1',
                marker_color='gray'
            )
        )
        # add vertical line for 0
        figure_sigmoid.add_trace(
            go.Scatter(
                x=[0, 0],
                y=[-.1, 1.1],
                mode='lines',
                name='v0',
                marker_color='gray'
            )
        )
        # add center point (0, 0.5)
        figure_sigmoid.add_trace(
            go.Scatter(
                x=[0],
                y=[0.5],
                mode='markers',
                name='center',
                marker_color='black'
            )
        )

    def plot_errors(self, errors: List[float]):
        self.figure_2d_error.add_trace(
            go.Scatter(
                x=list(range(len(errors))),
                y=errors,
                mode='lines',
                name='error',
                marker_color='red',
            )
        )
        # add axis lines
        self.figure_2d_error.add_trace(
            go.Scatter(
                x=[-1, len(errors) - 1],
                y=[0, 0],
                mode='lines',
                name='x',
                marker_color='gray'
            )
        )
        self.figure_2d_error.add_trace(
            go.Scatter(
                x=[0, 0],
                y=[-.01, max(errors) + .1],
                mode='lines',
                name='y',
                marker_color='gray'
            )
        )

    def save(self, path: str = './'):
        self.figure_2d_error.write_html(f"{path}figure_2d_data.html", auto_open=True)
        self.figure_2d_error.write_html(f"{path}figure_2d_error.html", auto_open=True)

    def show(self):
        self.figure_2d_data.show()
        self.figure_2d_error.show()