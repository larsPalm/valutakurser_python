from plotly.offline import plot
import plotly.graph_objects as go
from random import randint
import matplotlib.pyplot as plt
import datetime
from .get_stored import get_dates, get_a_cur, compare_2_cur, get_dates_rent


def get_mult__with_dates(from_cur, to_cur):
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


def make_matplot_plot_mult(values, x_values, title, min_val, max_val):
    fig2 = plt.figure()
    for key in values:
        plt.plot(x_values, values[key], label=key)
    plt.title(title)
    plt.legend()
    plt.ylim(min_val, max_val)
    plt.xlim([x_values[0], x_values[-1]])
    fig2.savefig('response2.png')


def make_plotly_plot_mult(values, x_values, title, min_val, max_val):
    graphs = []
    for elm in values:
        fig = go.Scatter(x=x_values, y=values[elm], mode='lines', name=elm)
        graphs.append(fig)
    layout = go.Layout(title=title,
                       yaxis=dict(range=[min_val, max_val]))
    plot_div = plot({'data': graphs, 'layout': layout},
                    output_type='div')
    return plot_div


def plot_compare_2_cur(from_cur, to_cur):
    graphs = []
    graph_value, x_values = compare_2_cur(from_cur, to_cur)
    fig = go.Scatter(x=x_values, y=graph_value, mode='lines', fill='tozeroy')
    graphs.append(fig)
    layout = go.Layout(title='{} vs {}'.format(from_cur, to_cur),
                       yaxis=dict(range=[min(graph_value), max(graph_value)]))
    return plot({'data': graphs, 'layout': layout}, output_type='div')


def plot_rents(rent_values):
    colors = '''
            aliceblue, aqua, aquamarine, azure,
            beige, bisque, black, blanchedalmond, blue,
            blueviolet, brown, burlywood, cadetblue,
            chartreuse, chocolate, cornflowerblue,
            cornsilk, crimson, cyan, darkblue, darkcyan,
            darkgoldenrod, darkgray, darkgrey, darkgreen,
            darkkhaki, darkmagenta, darkolivegreen, darkorange,
            darkorchid, darkred, darksalmon, darkseagreen,
            darkslateblue, darkslategray, darkslategrey,
            darkturquoise, darkviolet, deepskyblue,
            dimgray, dimgrey, dodgerblue, firebrick,
            forestgreen, fuchsia, gainsboro,
            gold, goldenrod, gray, green,
            greenyellow, honeydew, indianred, indigo,
            khaki, lavender, lavenderblush, lawngreen,
            lemonchiffon, lime, limegreen,
            linen, magenta, maroon, mediumaquamarine,
            mediumblue, mediumorchid, mediumpurple,
            mediumseagreen, mediumslateblue, mediumspringgreen,
            mediumturquoise, mediumvioletred, midnightblue,
            mistyrose, moccasin, navy,
            oldlace, olive, olivedrab, orange, orangered,
            orchid, palegoldenrod, palegreen, paleturquoise,
            palevioletred, papayawhip, peachpuff, peru,
            plum, powderblue, purple, red, rosybrown,
            royalblue, saddlebrown, sandybrown,
            seagreen, seashell, sienna,
            slateblue, slategray, slategrey, springgreen,
            steelblue, teal, thistle, tomato, turquoise,
            violet, yellow, yellowgreen'''.replace('\n        ', '').replace('\t', '').replace(' ', '').split(',')
    colors = """darkblue, darkcyan,
            darkgoldenrod, darkgray, darkgrey, darkgreen,
            darkkhaki, darkmagenta, darkorange,
            darkorchid, darkred, darksalmon, darkseagreen,
            darkslateblue, darkslategray, darkslategrey,
            darkturquoise, darkviolet, deepskyblue,
            navy, red, green""".replace('\n        ', '').replace('\t', '').replace(' ', '').split(',')
    used_nr = []
    graphs = []
    for elm in rent_values:
        number = randint(0, len(colors)-1)
        while number in used_nr:
            number = randint(0, len(colors))
            used_nr.append(number)
        x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in rent_values[elm].keys()]
        if elm == "KPRA":
            print(list(rent_values[elm].keys()))
        fig = go.Scatter(x=x_values, y=list(rent_values[elm].values()), mode='lines', name=elm,
                         marker=dict(color=colors[number], size=5))
        graphs.append(fig)
    layout = go.Layout(title='rents',)
    return plot({'data': graphs, 'layout': layout},
                    output_type='div')


def plot_rent_vs_nok(x_val_cur, y_val_cur, rent_data):
    rent_values = list(rent_data.values())
    rent_indices = list(rent_data.keys())
    rent_indices = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in rent_indices]
    graphs = []
    fig = go.Scatter(x=x_val_cur, y=list(y_val_cur), mode='lines', name="NOK vs SEK",
                     marker=dict(color='blue', size=5))
    graphs.append(fig)
    fig = go.Scatter(x=rent_indices, y=list(rent_values), mode='lines', name="KPRA",
                     marker=dict(color='red', size=5))
    graphs.append(fig)
    layout = go.Layout(title='The rent vs NOK', )
    return plot({'data': graphs, 'layout': layout},
                output_type='div')
