from flask import Flask, render_template, request, Markup
import json

app = Flask(__name__)

@app.route("/")
def render_home():
    return render_template('home.html')

@app.route("/p1r")
def render_resp1():
    with open('food_access.json') as food_access_data:
        place = json.load(food_access_data)
    if 'county' in request.args:
        county = request.args['county']
        data = get_data(place, county)
        population = None
        for p in place:
            if p["County"] == county:
                population = p.get("Population")
                break
        return render_template('popualarity_and_housing.html', place=data, population=population)

    return render_template('page1.html', options=get_county_options(place))

def get_data(place, county):
    infos = []
    data = []
    for p in place:
        info = p["County"]
        if p["County"] == county and info not in infos:
            infos.append(info)
            data.append({
                "Residing in Group Quarters": p["Housing Data"]["Residing in Group Quarters"]
            })
    return data

def get_county_options(place):
    counties = []
    options = ""
    for p in place:
        county = p["County"]
        if county not in counties:
            counties.append(county)
            options += Markup("<option value=\"" + str(county) + "\">" + str(county) + "</option>")
    return options

@app.route("/p2")
def render_page2():
    with open('food_access.json') as food_access_data:
        human = json.load(food_access_data)
    if 'State' in request.args:
        state = request.args['State']
        resident = get_resi_data(human, state)

        return render_template('stateres.html', human=get_resi_options(human), resident=resident)

    return render_template('page2.html', options=get_resi_options(human))

def get_resi_options(human):
    states = []
    options = ""
    for h in human:
        state = h["State"]
        if state not in states:
            states.append(state)
            options += Markup("<option value=\"" + str(state) + "\">" + str(state) + "</option>")
    return options

def get_resi_data(human, state):
    resi_data = None
    for h in human:
        if h["State"] == state:
            resi_data = h["Housing Data"]["Residing in Group Quarters"]
            break
    return resi_data

@app.route("/p3")
def render_page3():
    with open('food_access.json') as food_access_data:
        data = json.load(food_access_data)
    return render_template('pop_graph.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

