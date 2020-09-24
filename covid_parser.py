# Copyright (C) 2020 Alex Verrico (https://AlexVerrico.com/)
# Australian covid statistics are provided by https://covid19data.com.au/

import urllib.request
import json


aus_locations = {'aus': 1, 'nsw': 1, 'vic': 2, 'qld': 3, 'sa': 4, 'wa': 5, 'tas': 6, 'nt': 7, 'act': 8}
supported_data_types = ['cases', 'deaths', 'recoveries']
aus_states = {'nsw': 2, 'vic': 0, 'qld': 4, 'sa': 6, 'wa': 7, 'tas': 8, 'nt': 9, 'act': 10}


def rreplace(s, old, _new, occurrence):
    li = s.rsplit(old, occurrence)
    return _new.join(li)


def download_data(url):
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')
    return data


def get_state_new(data_type='cases'):
    if data_type == 'cases':
        data = download_data(r'https://infogram.com/1p0lp9vmnqd3n9te63x3q090ketnx57evn5?live')
        junk, data = data.split('dbf","chart_type_nr":10,"data":[')
        data, junk = data.split('],"custom":{"showPoints":true')
        data = data.replace(r'\u002F', '/')
        statedata = json.loads(data)
        return statedata
    elif data_type == 'deaths':
        data = download_data(r'https://e.infogram.com/90ab7c54-efe3-4d76-a3f6-19c8544249e4?live')
        junk, data = data.split('a3b","chart_type_nr":10,"data":[')
        data, junk = data.split('],"custom":{"showPoints":false')
        data = data.replace(r'\u002f', '/')
        statedata = json.loads(data)
        return statedata
    elif data_type == 'recoveries':
        data = download_data(r'https://e.infogram.com/_/1x9ogDI1RFHnyzW4sfFx?live')
        junk, data = data.split(r'c19","chart_type_nr":1,"data":', 1)
        data, junk = data.split(r',"custom":{"showPoints":true,"', 1)
        data = data.replace(r'\u002F', '/')
        data = json.loads(data)
        statedata = list()
        for i in range(1, len(data[aus_states['nsw']])):
            tmp = [data[aus_states['nsw']][i][0], data[aus_states['nsw']][i][2], data[aus_states['vic']][i][2],
                   data[aus_states['qld']][i][2], data[aus_states['sa']][i][2], data[aus_states['wa']][i][2],
                   data[aus_states['tas']][i][2], data[aus_states['nt']][i][2], data[aus_states['act']][i][2]]
            statedata.append(tmp)
        return statedata


def get_aus_new(data_type='cases'):
    if data_type == 'cases':
        data = download_data(r'https://infogram.com/1p7ve7kjeld1pebz2nm0vpqv7nsnp92jn2x?live')
        junk, data = data.split('a7e","chart_type_nr":1,"data":[')
        data, junk = data.split('],"custom":{"showPoints":true')
        data = data.replace(r'\u002F', '/')
        ausdata = json.loads(data)
        return ausdata
    elif data_type == 'deaths':
        data = download_data(r'https://e.infogram.com/154e01ec-a6e7-45da-8fcf-d6c9a6669ba8?live')
        junk, data = data.split('aae","chart_type_nr":1,"data":[')
        data, junk = data.split('],"custom":{"showPoints":false')
        data = data.replace(r'\u002F', '/')
        ausdata = json.loads(data)
        return ausdata
    elif data_type == 'recoveries':
        data = download_data(r'https://e.infogram.com/_/1x9ogDI1RFHnyzW4sfFx?live')
        junk, data = data.split(r'c19","chart_type_nr":1,"data":', 1)
        data, junk = data.split(r',"custom":{"showPoints":true,"', 1)
        data = data.replace(r'\u002F', '/')
        data = data.replace('""', '"0"')
        data = json.loads(data)
        ausdata = list()
        for i in range(1, len(data[aus_states['nsw']])):
            tmp = [data[aus_states['nsw']][i][0], str(int(data[aus_states['nsw']][i][2].replace(',', '')) +
                   int(data[aus_states['vic']][i][2].replace(',', '')) +
                   int(data[aus_states['qld']][i][2].replace(',', '')) +
                   int(data[aus_states['sa']][i][2].replace(',', '')) +
                   int(data[aus_states['wa']][i][2].replace(',', '')) +
                   int(data[aus_states['tas']][i][2].replace(',', '')) +
                   int(data[aus_states['nt']][i][2].replace(',', '')) +
                   int(data[aus_states['act']][i][2].replace(',', '')))]
            ausdata.append(tmp)
        return ausdata


def get_country_new(country='australia', data_type='cases'):
    data = download_data(r'https://epidemic-stats.com/coronavirus/%s' % country)
    if data_type == 'cases':
        junk, data = data.split('infected_new = ')
        data, junk = data.split('const recovered_new = ')
        data = data.replace("'", '"')
        data = rreplace(data, ',', '', 1)
        countrydata = json.loads(data)
        return countrydata
    elif data_type == 'deaths':
        junk, data = data.split('deaths_new = ')
        data, junk = data.split('const infected_new = ')
        data = data.replace("'", '"')
        data = rreplace(data, ',', '', 1)
        countrydata = json.loads(data)
        return countrydata
    elif data_type == 'recoveries':
        junk, data = data.split('const recovered_new = ')
        data, junk = data.split('const current_infected = ')
        data = data.replace("'", '"')
        data = rreplace(data, ',', '', 1)
        countrydata = json.loads(data)
        return countrydata


def new_cases(location='aus'):  # Depreciated, use new(location=location, data_type='cases')
    if location in aus_locations:
        if location == 'aus':
            data = get_aus_new()
        else:
            data = get_state_new()
        parsed_data = [data[-1][aus_locations[location]], data[-2][aus_locations[location]]]
    elif location == 'usa':
        data = get_country_new('usa')
        parsed_data = [data[-1], data[-2]]
    else:
        try:
            data = get_country_new(location)
            parsed_data = [data[-1], data[-2]]
        except urllib.error.HTTPError:
            parsed_data = "unsupportedLocation"
    return parsed_data


def new_deaths(location='aus'):  # Depreciated, use new(location=location, data_type='cases')
    if location in aus_locations:
        if location == 'aus':
            data = get_aus_new(data_type='deaths')
        else:
            data = get_state_new(data_type='deaths')
        parsed_data = [data[-1][aus_locations[location]], data[-2][aus_locations[location]]]
    elif location == 'usa':
        data = get_country_new('usa', data_type='deaths')
        parsed_data = [data[-1], data[-2]]
    else:
        try:
            data = get_country_new(location)
            parsed_data = [data[-1], data[-2]]
        except urllib.error.HTTPError:
            parsed_data = "unsupportedLocation"
    return parsed_data


def new(location='aus', data_type='cases'):
    if data_type not in supported_data_types:
        return "unsupportedDataType"
    else:
        if location in aus_locations:
            if location == 'aus':
                data = get_aus_new(data_type=data_type)
            else:
                data = get_state_new(data_type=data_type)
            parsed_data = [data[-1][aus_locations[location]], data[-2][aus_locations[location]]]
        else:
            try:
                data = get_country_new(location, data_type=data_type)
                parsed_data = [data[-1], data[-2]]
            except urllib.error.HTTPError:
                parsed_data = "unsupportedLocation"
        return parsed_data


# def total(location='aus', data_type='cases'):
#     print(location)

# print(new(data_type='recoveries', location='china'))
