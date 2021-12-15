from plotly.offline import plot,plot_mpl
import plotly.graph_objects as go
from random import randint
import matplotlib.pyplot as plt
import io, base64
from .get_stored import *
from .validate_input import *


def get_mult__with_dates(from_cur,to_cur):
    x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in get_dates()]
    cur1 = get_a_cur(from_cur)
    cur2 = get_a_cur(to_cur)
    graph_value = [round(v1 / v2, 4) for v1, v2 in zip(cur1, cur2)]
    title = '{} vs {}'.format(from_cur, to_cur)
    colors1 = ['b', "g", 'r', 'c', "m", "y", 'k']
    colors2 = ["blue", "green", 'red', "cyan", "magenta", 'yellow', 'black']
    index = randint(0, len(colors1) - 1)
    fig2 = plt.figure()
    plt.plot(x_values, graph_value, colors1[index])
    plt.fill_between(x_values, graph_value, color=colors2[index], alpha=0.5)
    plt.title(title)
    plt.ylim(min(graph_value), max(graph_value))
    plt.xlim([x_values[0], x_values[-1]])
    fig2.savefig('response.png')


def make_matplot_plot_mult(values,x_values,title,min_val,max_val):
    fig2 = plt.figure()
    for key in values:
        plt.plot(x_values, values[key], label=key)
    plt.title(title)
    plt.legend()
    plt.ylim(min_val, max_val)
    plt.xlim([x_values[0], x_values[-1]])
    fig2.savefig('response2.png')


def make_plotly_plot_mult(values,x_values,title,min_val,max_val):
    graphs = []
    for elm in values:
        fig = go.Scatter(x=x_values, y=values[elm], mode='lines', name=elm)
        graphs.append(fig)
    layout = go.Layout(title=title,
                       yaxis=dict(range=[min_val, max_val]))
    plot_div = plot({'data': graphs, 'layout': layout},
                    output_type='div')
    return plot_div


def plot_compare_2_cur(from_cur,to_cur):
    graphs = []
    graph_value, x_values = compare_2_cur(from_cur, to_cur)
    fig = go.Scatter(x=x_values, y=graph_value, mode='lines', fill='tozeroy')
    graphs.append(fig)
    layout = go.Layout(title='{} vs {}'.format(from_cur, to_cur),
                       yaxis=dict(range=[min(graph_value), max(graph_value)]))
    return plot({'data': graphs, 'layout': layout}, output_type='div')
