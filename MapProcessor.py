import folium
from folium.plugins import HeatMap, MarkerCluster
from geopy.geocoders import ArcGIS
import os.path
import random

path = 'maindata.txt'
grads = [('red', 'blue', 'green'), ('purple', 'orange', 'darkred'),
         ('lightred', 'beige', 'darkblue'), ('darkgreen', 'cadetblue',
                                             'darkpurple'),
         ('white', 'pink', 'lightblue'), ('lightgreen',
                                          'gray', 'black')]


def reader(pt=path):
    """
    Read file with events
    :param pt: path to file
    :return: list of events
    """
    data = open(pt, encoding='utf-8', errors='ignore').read()
    data = data.split("####")
    events = [i.strip().split('@@') for i in data]
    return events


def position_finder():
    """
    Replace places from text to lng lat
    :return: None, writes to file bdata
    """
    events = reader()
    with open('bdata.txt', 'w', errors='ignore', encoding='utf-8')as file:
        geolocator = ArcGIS(timeout=10)
        for event in events:
            if type(event[0]) != tuple:
                loc = geolocator.geocode(event[0])
                event[0] = (loc.latitude, loc.longitude)
            file.write('{}@@{}@@{}@@{}@@{}@@{}@@{}####'.format(
                *[event[i] for i in range(7)]))


def events_by_category():
    """
    Makes a dict with category as key and events of this category as value
    :return: dict
    """
    events = reader('bdata.txt')
    category_dict = dict()
    for event in events:
        if len(event) < 7:
            continue
        if event[2] in category_dict:
            category_dict[event[2]] += [event]
        else:
            category_dict[event[2]] = [event]
    return category_dict


# def little_hack(evs):
#     def get_number():
#         if random.random() <= 0.3:
#             return 0
#         else:
#             return 1
#
#     for i in evs:
#         for j in evs[i]:
#             j.append(get_number())

def build_heat_map(events, param=False):
    """
    Build heat map by given dict of categories
    :param events:
    :return:
    """

    def heat_layer(cat):
        grad = grads[color % 6]
        by_category = events[cat]
        # list with locations
        heatdata = [eval(event[0]) for event in by_category]
        HeatMap(heatdata, name=cat,
                gradient={.3: grad[0], .65: grad[1], .1: grad[2]}
                ).add_to(event_map)

    event_map = folium.Map(zoom_start=10, tiles='OpenStreetMap',
                           location=[49.84441000000004, 24.02543000000003])
    color = 0
    if not param:
        for k in events:
            heat_layer(k)
            color += 1
    else:
        heat_layer(param)
    return event_map.save(os.path.join(
        'C:\programming\CourseWork\\templates', 'wrldheatmap.html'))


def build_reg_map(events, param=False):
    """
    Build regular map buy given dict of categories
    :param events:
    :return:
    """
    def event_layer(cat):
        markers = MarkerCluster(name=cat).add_to(event_map)
        for event in events[cat]:
            pop = (
                "{category}<br>"
                "FB: {facebook}<br>"
                "Start Time: {time}<br>"
            ).format(category=str(event[2]),
                     facebook=str(event[3]),
                     time=str(event[4]))
            event[0] = eval(event[0])
            folium.Marker(location=[float(event[0][0]), float(event[0][1])],
                          popup=pop,
                          icon=folium.Icon()).add_to(markers)
        event_map.add_child(markers)
    event_map = folium.Map(zoom_start=8, tiles='OpenStreetMap',
                           location=[49.84441000000004, 24.02543000000003])
    if not param:
        for k in events:
            event_layer(k)
    else:
        event_layer(param)
    event_map.add_child(folium.LayerControl())
    return event_map.save(
        os.path.join('C:\programming\CourseWork\\templates',
                     'wrldregmap.html'))
