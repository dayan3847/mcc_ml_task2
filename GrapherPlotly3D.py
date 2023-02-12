from typing import List
import numpy as np
import plotly.graph_objs as go
from plotly.graph_objs import Figure

from Artificial import Artificial
from GrapherPlotly import GrapherPlotly
from Polynomial import Polynomial


class GrapherPlotly3D(GrapherPlotly):

    def __init__(self):
        super().__init__()

        self.figure_3d_data: Figure = go.Figure()
        self.figure_3d_data.update_layout(
            scene=dict(
                xaxis_title='x0',
                yaxis_title='x1',
                zaxis_title='y',
                xaxis_range=self.area_to_pot[0],
                yaxis_range=self.area_to_pot[1],
                zaxis_range=self.area_to_pot[2],
            ),
            showlegend=True,
        )

    def plot_artificial_data_3d(self, artificial: List[Artificial], show: bool = False):
        x0_list = []
        x1_list = []
        y_list = []
        for data in artificial:
            x0_list.append(data.x_list_data[0])
            x1_list.append(data.x_list_data[1])
            y_list.append(data.y_data)
        self.figure_3d_data.add_trace(
            go.Scatter3d(
                x=x0_list,
                y=x1_list,
                z=y_list,
                mode='markers',
                marker=dict(size=12, color=y_list, opacity=0.8, colorscale='Viridis'),
                name='Points',
            )
        )
        if show:
            self.figure_3d_data.show()

    def plot_polynomial_3d(self, polinomial: Polynomial, show: bool = False):
        if polinomial.get_variables_count() > 3:
            return
        x0 = self.data_to_pot['x0']
        x1 = self.data_to_pot['x1']
        y = polinomial.evaluate([x0, x1])
        self.figure_3d_data.add_trace(
            go.Surface(
                z=y,
                x=x0,
                y=x1,
                opacity=0.5,
                showscale=False,
                colorscale='Oranges',
                name='Initial',
                showlegend=True,
            )
        )
        if show:
            self.figure_3d_data.show()

    # graficar el plano y = 0
    def plot_plane_y0(self, show: bool = False):
        x0 = self.data_to_pot['x0']
        x1 = self.data_to_pot['x1']
        y = np.zeros(x0.shape)
        self.figure_3d_data.add_trace(
            go.Surface(
                z=y,
                x=x0,
                y=x1,
                opacity=0.3,
                showscale=False,
                colorscale='Greys',
                name='Plane y = 0',
                showlegend=True,
            )
        )
        if show:
            self.figure_3d_data.show()

    def plot_polynomial_projection_3d(self, polinomial: Polynomial, show: bool = False):
        if polinomial.get_variables_count() > 2:
            return
        if polinomial.get_last_variable_degree() > 1:
            return
        x0_list = np.linspace(-3, 3, 100)
        x1_list = []
        for x0 in x0_list:
            x1 = polinomial.evaluate_despejando([x0], 1)
            x1_list.append(x1)

        x0_list, x1_list, y_list_zeros = np.meshgrid(x0_list, x1_list, [0])

        self.figure_3d_data.add_trace(
            go.Scatter3d(x=x0_list, y=x1_list, mode='lines', name='Polinomial', marker_color='green')
        )
        if show:
            self.figure_3d_data.show()
