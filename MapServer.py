from flask import Flask, render_template, request
import MapProcessor
import time
import Parser

refreshtime = time.time()
first = 1

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEAMPLATES_AUTO_RELOAD'] = True


def refreshall():
    global first
    #if first != 1:
        # Parser.start()
    first = 0
    MapProcessor.position_finder()
    events = MapProcessor.events_by_category()
    MapProcessor.build_heat_map(events)
    MapProcessor.build_reg_map(events)


@app.route("/")
def start_page():
    return render_template("startpage.html")


@app.route("/heatmap", methods=['POST'])
def heatmap():
    global refreshtime
    if (time.time() - refreshtime) > 86400:
        refreshtime = time.time()
        refreshall()
    if request.form["cat2"] != '':
        MapProcessor.build_heat_map(MapProcessor.events_by_category(),
                                    param=request.form["cat2"])
    else:
        MapProcessor.build_heat_map(MapProcessor.events_by_category())
    return render_template("wrldheatmap.html")


@app.route("/regmap", methods=['POST'])
def regmap():
    global refreshtime
    if (time.time() - refreshtime) > 86400:
        refreshtime = time.time()
        refreshall()
    if request.form["cat1"] != '':
        MapProcessor.build_reg_map(MapProcessor.events_by_category(),
                                    param=request.form["cat1"])
    else:
        MapProcessor.build_reg_map(MapProcessor.events_by_category())
    return render_template("wrldregmap.html")


refreshall()
app.run(debug=True)
