##############################################
#### Updated By: SATYAKI DE               ####
#### Updated On: 02-Oct-2021              ####
####                                      ####
#### Objective: Consuming Streaming data  ####
#### from Ably channels & captured IOT    ####
#### events from the simulator & publish  ####
#### them in Dashboard through measured   ####
#### KPIs.                                ####
####                                      ####
##############################################

import os
import pathlib
import numpy as np
import datetime as dt
import dash
from dash import dcc
from dash import html
import datetime

import dash_daq as daq

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from scipy.stats import rayleigh

# Consuming data from Ably Queue
from ably import AblyRest

# Main Class to consume streaming
import clsStreamConsume as ca

# Create the instance of the Covid API Class
x1 = ca.clsStreamConsume()

var1 = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
print('*' *60)
DInd = 'Y'

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "IOT Device Dashboard"

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H4("IOT DEVICE STREAMING", className="app__header__title"),
                        html.P(
                            "This app continually consumes streaming data from IOT-Device and displays live charts of various metrics & KPI associated with it.",
                            className="app__header__title--grey",
                        ),
                    ],
                    className="app__header__desc",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("SOURCE CODE", className="link-button"),
                            href="https://github.com/SatyakiDe2019/IOTStream",
                        ),
                        html.A(
                            html.Button("VIEW DEMO", className="link-button"),
                            href="https://github.com/SatyakiDe2019/IOTStream/blob/main/demo.gif",
                        ),
                        html.A(
                            html.Img(
                                src=app.get_asset_url("dash-new-logo.png"),
                                className="app__menu__img",
                            ),
                            href="https://plotly.com/dash/",
                        ),
                    ],
                    className="app__header__logo",
                ),
            ],
            className="app__header",
        ),
        html.Div(
            [
                # Motor Speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("SERVO METER (IOT)", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="iot-measure",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ),
                        ),
                        dcc.Interval(
                            id="iot-measure-update",
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        ),
                        # Second Panel
                        html.Div(
                            [html.H6("DC-MOTOR (IOT)", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="iot-measure-1",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ),
                        ),
                        dcc.Interval(
                            id="iot-measure-update-1",
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        )
                    ],
                    className="two-thirds column motor__speed__container",
                ),
                html.Div(
                    [
                        # histogram
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "MOTOR POWER HISTOGRAM",
                                            className="graph__title",
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        dcc.Slider(
                                            id="bin-slider",
                                            min=1,
                                            max=60,
                                            step=1,
                                            value=20,
                                            updatemode="drag",
                                            marks={
                                                20: {"label": "20"},
                                                40: {"label": "40"},
                                                60: {"label": "60"},
                                            },
                                        )
                                    ],
                                    className="slider",
                                ),
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id="bin-auto",
                                            options=[
                                                {"label": "Auto", "value": "Auto"}
                                            ],
                                            value=["Auto"],
                                            inputClassName="auto__checkbox",
                                            labelClassName="auto__label",
                                        ),
                                        html.P(
                                            "# of Bins: Auto",
                                            id="bin-size",
                                            className="auto__p",
                                        ),
                                    ],
                                    className="auto__container",
                                ),
                                dcc.Graph(
                                    id="motor-histogram",
                                    figure=dict(
                                        layout=dict(
                                            plot_bgcolor=app_color["graph_bg"],
                                            paper_bgcolor=app_color["graph_bg"],
                                        )
                                    ),
                                ),
                            ],
                            className="graph__container first",
                        ),
                        # motor direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "SERVO MOTOR DIRECTION", className="graph__title"
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="servo-motor-direction",
                                    figure=dict(
                                        layout=dict(
                                            plot_bgcolor=app_color["graph_bg"],
                                            paper_bgcolor=app_color["graph_bg"],
                                        )
                                    ),
                                ),
                            ],
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
    ],
    className="app__container",
)

def toPositive(row, flag):
    try:
        if flag == 'ServoMeter':
            x_val = abs(float(row['ServoMotor']))
        elif flag == 'DCMotor':
            x_val = abs(float(row['DCMotor'])) * 0.001

        return x_val

    except Exception as e:
        x = str(e)
        print(x)

        val = 0

        return val

def toPositiveInflated(row, flag):
    try:
        if flag == 'ServoMeter':
            x_val = abs(float(row['ServoMeter'])) * 100
        elif flag == 'DCMotor':
            x_val = abs(float(row['DCMeter'])) * 100

        return x_val

    except Exception as e:
        x = str(e)
        print(x)

        val = 0

        return val

def getData(var, Ind):
    try:
        # Let's pass this to our map section
        df = x1.conStream(var, Ind)

        df['ServoMeterNew'] = df.apply(lambda row: toPositiveInflated(row, 'ServoMeter'), axis=1)
        df['ServoMotorNew'] = df.apply(lambda row: toPositive(row, 'ServoMeter'), axis=1)
        df['DCMotor'] = df.apply(lambda row: toPositiveInflated(row, 'DCMotor'), axis=1)
        df['DCMeterNew'] = df.apply(lambda row: toPositive(row, 'DCMotor'), axis=1)

        # Dropping old columns
        df.drop(columns=['ServoMeter','ServoMotor','DCMeter'], axis=1, inplace=True)

        #Rename New Columns to Old Columns
        df.rename(columns={'ServoMeterNew':'ServoMeter'}, inplace=True)
        df.rename(columns={'ServoMotorNew':'ServoMotor'}, inplace=True)
        df.rename(columns={'DCMeterNew':'DCMeter'}, inplace=True)

        return df
    except Exception as e:
        x = str(e)
        print(x)

        df = p.DataFrame()

        return df

@app.callback(
    Output("iot-measure-1", "figure"), [Input("iot-measure-update", "n_intervals")]
)
def gen_iot_speed(interval):
    """
    Generate the DC Meter graph.
    :params interval: update the graph based on an interval
    """

    # Let's pass this to our map section
    df = getData(var1, DInd)

    trace = dict(
        type="scatter",
        y=df["DCMotor"],
        line={"color": "#42C4F7"},
        hoverinfo="skip",
        error_y={
            "type": "data",
            "array": df["DCMeter"],
            "thickness": 1.5,
            "width": 2,
            "color": "#B4E8FC",
        },
        mode="lines",
    )

    layout = dict(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        height=400,
        xaxis={
            "range": [0, 200],
            "showline": True,
            "zeroline": False,
            "fixedrange": True,
            "tickvals": [0, 50, 100, 150, 200],
            "ticktext": ["200", "150", "100", "50", "0"],
            "title": "Time Elapsed (sec)",
        },
        yaxis={
            "range": [
                min(0, min(df["DCMotor"])),
                max(100, max(df["DCMotor"]) + max(df["DCMeter"])),
            ],
            "showgrid": True,
            "showline": True,
            "fixedrange": True,
            "zeroline": False,
            "gridcolor": app_color["graph_line"],
            "nticks": max(6, round(df["DCMotor"].iloc[-1] / 10)),
        },
    )

    return dict(data=[trace], layout=layout)

@app.callback(
    Output("iot-measure", "figure"), [Input("iot-measure-update", "n_intervals")]
)
def gen_iot_speed(interval):
    """
    Generate the Motor Speed graph.
    :params interval: update the graph based on an interval
    """

    # Let's pass this to our map section
    df = getData(var1, DInd)

    trace = dict(
        type="scatter",
        y=df["ServoMeter"],
        line={"color": "#42C4F7"},
        hoverinfo="skip",
        error_y={
            "type": "data",
            "array": df["ServoMotor"],
            "thickness": 1.5,
            "width": 2,
            "color": "#B4E8FC",
        },
        mode="lines",
    )

    layout = dict(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        height=400,
        xaxis={
            "range": [0, 200],
            "showline": True,
            "zeroline": False,
            "fixedrange": True,
            "tickvals": [0, 50, 100, 150, 200],
            "ticktext": ["200", "150", "100", "50", "0"],
            "title": "Time Elapsed (sec)",
        },
        yaxis={
            "range": [
                min(0, min(df["ServoMeter"])),
                max(100, max(df["ServoMeter"]) + max(df["ServoMotor"])),
            ],
            "showgrid": True,
            "showline": True,
            "fixedrange": True,
            "zeroline": False,
            "gridcolor": app_color["graph_line"],
            "nticks": max(6, round(df["ServoMeter"].iloc[-1] / 10)),
        },
    )

    return dict(data=[trace], layout=layout)


@app.callback(
    Output("servo-motor-direction", "figure"), [Input("iot-measure-update", "n_intervals")]
)
def gen_motor_direction(interval):
    """
    Generate the Servo direction graph.
    :params interval: update the graph based on an interval
    """

    df = getData(var1, DInd)
    val = df["ServoMeter"].iloc[-1]
    direction = [0, (df["ServoMeter"][0]*100 - 20), (df["ServoMeter"][0]*100 + 20), 0]

    traces_scatterpolar = [
        {"r": [0, val, val, 0], "fillcolor": "#084E8A"},
        {"r": [0, val * 0.65, val * 0.65, 0], "fillcolor": "#B4E1FA"},
        {"r": [0, val * 0.3, val * 0.3, 0], "fillcolor": "#EBF5FA"},
    ]

    data = [
        dict(
            type="scatterpolar",
            r=traces["r"],
            theta=direction,
            mode="lines",
            fill="toself",
            fillcolor=traces["fillcolor"],
            line={"color": "rgba(32, 32, 32, .6)", "width": 1},
        )
        for traces in traces_scatterpolar
    ]

    layout = dict(
        height=350,
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        autosize=False,
        polar={
            "bgcolor": app_color["graph_line"],
            "radialaxis": {"range": [0, 45], "angle": 45, "dtick": 10},
            "angularaxis": {"showline": False, "tickcolor": "white"},
        },
        showlegend=False,
    )

    return dict(data=data, layout=layout)


@app.callback(
    Output("motor-histogram", "figure"),
    [Input("iot-measure-update", "n_intervals")],
    [
        State("iot-measure", "figure"),
        State("bin-slider", "value"),
        State("bin-auto", "value"),
    ],
)
def gen_motor_histogram(interval, iot_speed_figure, slider_value, auto_state):
    """
    Genererate iot histogram graph.
    :params interval: upadte the graph based on an interval
    :params iot_speed_figure: current Motor Speed graph
    :params slider_value: current slider value
    :params auto_state: current auto state
    """

    motor_val = []

    try:
        print('Inside gen_motor_histogram:')
        print('iot_speed_figure::')
        print(iot_speed_figure)

        # Check to see whether iot-measure has been plotted yet
        if iot_speed_figure is not None:
            motor_val = iot_speed_figure["data"][0]["y"]
        if "Auto" in auto_state:
            bin_val = np.histogram(
                motor_val,
                bins=range(int(round(min(motor_val))), int(round(max(motor_val)))),
            )
        else:
            bin_val = np.histogram(motor_val, bins=slider_value)
    except Exception as error:
        raise PreventUpdate

    avg_val = float(sum(motor_val)) / len(motor_val)
    median_val = np.median(motor_val)

    pdf_fitted = rayleigh.pdf(
        bin_val[1], loc=(avg_val) * 0.55, scale=(bin_val[1][-1] - bin_val[1][0]) / 3
    )

    y_val = (pdf_fitted * max(bin_val[0]) * 20,)
    y_val_max = max(y_val[0])
    bin_val_max = max(bin_val[0])

    trace = dict(
        type="bar",
        x=bin_val[1],
        y=bin_val[0],
        marker={"color": app_color["graph_line"]},
        showlegend=False,
        hoverinfo="x+y",
    )

    traces_scatter = [
        {"line_dash": "dash", "line_color": "#2E5266", "name": "Average"},
        {"line_dash": "dot", "line_color": "#BD9391", "name": "Median"},
    ]

    scatter_data = [
        dict(
            type="scatter",
            x=[bin_val[int(len(bin_val) / 2)]],
            y=[0],
            mode="lines",
            line={"dash": traces["line_dash"], "color": traces["line_color"]},
            marker={"opacity": 0},
            visible=True,
            name=traces["name"],
        )
        for traces in traces_scatter
    ]

    trace3 = dict(
        type="scatter",
        mode="lines",
        line={"color": "#42C4F7"},
        y=y_val[0],
        x=bin_val[1][: len(bin_val[1])],
        name="Rayleigh Fit",
    )
    layout = dict(
        height=350,
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        xaxis={
            "title": "Motor Power",
            "showgrid": False,
            "showline": False,
            "fixedrange": True,
        },
        yaxis={
            "showgrid": False,
            "showline": False,
            "zeroline": False,
            "title": "Number of Samples",
            "fixedrange": True,
        },
        autosize=True,
        bargap=0.01,
        bargroupgap=0,
        hovermode="closest",
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "xanchor": "center",
            "y": 1,
            "x": 0.5,
        },
        shapes=[
            {
                "xref": "x",
                "yref": "y",
                "y1": int(max(bin_val_max, y_val_max)) + 0.5,
                "y0": 0,
                "x0": avg_val,
                "x1": avg_val,
                "type": "line",
                "line": {"dash": "dash", "color": "#2E5266", "width": 5},
            },
            {
                "xref": "x",
                "yref": "y",
                "y1": int(max(bin_val_max, y_val_max)) + 0.5,
                "y0": 0,
                "x0": median_val,
                "x1": median_val,
                "type": "line",
                "line": {"dash": "dot", "color": "#BD9391", "width": 5},
            },
        ],
    )
    return dict(data=[trace, scatter_data[0], scatter_data[1], trace3], layout=layout)


@app.callback(
    Output("bin-auto", "value"),
    [Input("bin-slider", "value")],
    [State("iot-measure", "figure")],
)
def deselect_auto(slider_value, iot_speed_figure):
    """ Toggle the auto checkbox. """

    # prevent update if graph has no data
    if "data" not in iot_speed_figure:
        raise PreventUpdate
    if not len(iot_speed_figure["data"]):
        raise PreventUpdate

    if iot_speed_figure is not None and len(iot_speed_figure["data"][0]["y"]) > 5:
        return [""]
    return ["Auto"]


@app.callback(
    Output("bin-size", "children"),
    [Input("bin-auto", "value")],
    [State("bin-slider", "value")],
)
def show_num_bins(autoValue, slider_value):
    """ Display the number of bins. """

    if "Auto" in autoValue:
        return "# of Bins: Auto"
    return "# of Bins: " + str(int(slider_value))


if __name__ == "__main__":
    app.run_server(debug=True)
