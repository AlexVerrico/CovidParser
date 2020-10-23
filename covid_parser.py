# Copyright (C) 2020 Alex Verrico (https://AlexVerrico.com/)
# Australian covid statistics are provided by https://covid19data.com.au/

import urllib.request
import json


aus_locations = {'aus': 1, 'nsw': 1, 'vic': 2, 'qld': 3, 'sa': 4, 'wa': 5, 'tas': 6, 'nt': 7, 'act': 8}
aus_states = {'nsw': 1, 'vic': 2, 'qld': 3, 'sa': 4, 'wa': 5, 'tas': 6, 'nt': 7, 'act': 8}
ausStates = {'nsw': 2, 'vic': 0, 'qld': 4, 'sa': 6, 'wa': 7, 'tas': 8, 'nt': 9, 'act': 10}
supported_data_types = ['cases', 'deaths', 'recoveries']


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
    # elif data_type == 'recoveries':
        # data = download_data(r'https://e.infogram.com/_/1x9ogDI1RFHnyzW4sfFx')
        # junk, data = data.split(r'c19","chart_type_nr":1,"data":', 1)
        # data, junk = data.split(r',"custom":{"showPoints":true,"', 1)
        # data = data.replace(r'\u002F', '/')
        # data = json.loads(data)
        # statedata = list()
        # print(data)
        # for i in range(0, len(data[aus_states['vic']])):
        #     tmp = [data[aus_states['nsw']][i][0], data[aus_states['nsw']][i][2], data[aus_states['vic']][i][2],
        #            data[aus_states['qld']][i][2], data[aus_states['sa']][i][2], data[aus_states['wa']][i][2],
        #            data[aus_states['tas']][i][2], data[aus_states['nt']][i][2], data[aus_states['act']][i][2]]
        #     statedata.append(tmp)
        # print(statedata)

        # data = download_data(r'https://e.infogram.com/_/ZPUD4Kmuso7AJ0jLaRlt')
        # junk, data = data.split(r'164","chart_type_nr":6,"data":', 1)
        # data, junk = data.split(r',"custom":{"showPoints":true,"', 1)
        # data = data.replace(r'\u002F', '/')
        # data = json.loads(data)
        # # print(data)
        # statedata = list()
        # for i in range(2, len(data[aus_states['vic']])):
        # # for i in range(2, 5):
        #     temp = list()
        #     tmp = list()
        #     iminus = i - 1
        #     # tmp = [data[aus_locations['nsw']][i][0], str(int(data[aus_locations['nsw']][iminus][1]) - int(data[aus_locations['nsw']][i][1])), data[aus_locations['vic']][i][1],
        #     #        data[aus_locations['qld']][i][1], data[aus_locations['sa']][i][1], data[aus_locations['wa']][i][1],
        #     #        data[aus_locations['tas']][i][1], data[aus_locations['nt']][i][1], data[aus_locations['act']][i][1]]
        #     # for x in aus_locations:
        #     #     tmp1 = data[aus_locations[x]][i]
        #     #     y = i - 1
        #     #     tmp2 = data[aus_locations[x]][y]
        #     #     print(tmp1)
        #     #     print(tmp2)
        #     #     print(str(int(tmp1[1]) - int(tmp2[1])))
        #     temp = data[aus_states['nsw']][i][0]
        #     tmp.append(temp)
        #     for loc in aus_states:
        #         temp = str(int(data[aus_locations[loc]][iminus][1].replace(',', '')) - int(data[aus_locations[loc]][i][1].replace(',', '')))
        #         tmp.append(temp)
        #     print(tmp)
        #     statedata.append(tmp)

        # vicdata = download_data(r'https://www.dhhs.vic.gov.au/victorian-coronavirus-covid-19-data')
        # junk, vicdata = vicdata.split("""<div class="lvn-body">
    	# 	<div class="row">
    	# 		<div class="col-xs-6 col-sm-3">
    	# 			<div class="lvn-box lvn-box-top">""")
        # vicdata, junk = vicdata.split("""</div>
    	# 			<div class="lvn-box lvn-box-bottom">
    	# 				<h4>782</h4>
    	# 				<p>total lives lost</p>
    	# 			</div>
    	# 		</div>
    	# 		<div class="col-xs-6 col-sm-3">""")
        # vicdata = vicdata.replace('\t', '')
        # vicdata = vicdata.split('\n')
        # print(vicdata)
        # # return statedata


def get_state_new_v2(data_type='cases', location='vic'):
    data = download_data(r"https://atlas.jifo.co/api/connectors/0b334273-5661-4837-a639-e3a384d81d20")
    data = json.loads(data)
    data = data["data"]
    if data_type == 'cases':
        data = data[8]
        return data
    if data_type == 'deaths':
        data = data[15]
        return data
    if data_type == 'recoveries':
        data1 = download_data(r'https://atlas.jifo.co/api/connectors/f3401355-a94b-4360-a1f8-1f23478840ad')
        data1 = json.loads(data1)
        statedata = list()
        for i in range(1, len(data1["data"][0])):
            tmp1 = list()
            tmp1.append('')
            for loc in ausStates:
                tmp = data1["data"][ausStates[loc]][i][2]
                tmp1.append(tmp)
            statedata.append(tmp1)
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
        ausdata = get_country_new('australia', data_type='recoveries')
        # print(ausdata)
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
            data = get_state_new_v2(data_type='cases')
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
            data = get_state_new_v2(data_type='deaths')
            print(data[-1])
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


def new(location='aus', data_type='cases', time='2days'):
    if data_type not in supported_data_types:
        return "unsupportedDataType"
    else:
        if location in aus_locations:

            if location == 'aus':
                if data_type == 'recoveries':
                    data = get_country_new('australia', data_type='recoveries')
                    if time == '2days':
                        parsed_data = [data[-1], data[-2]]
                    else:
                        parsed_data = list()
                        for i in range(1, len(data) + 1):
                            parsed_data.append(data[-i])
                    return parsed_data
                else:
                    data = get_aus_new(data_type=data_type)
            else:
                # if data_type == 'recoveries':
                #     return "unsupportedDataType"
                # else:
                data = get_state_new_v2(data_type=data_type, location=location)
            # print(data)
            if time == '2days':
                parsed_data = [data[-1][aus_locations[location]], data[-2][aus_locations[location]]]
            else:
                parsed_data = list()
                for i in range(1, len(data)):
                    parsed_data.append(data[-i][aus_locations[location]])
        else:
            try:
                data = get_country_new(location, data_type=data_type)
                parsed_data = [data[-1], data[-2]]
            except urllib.error.HTTPError:
                parsed_data = "unsupportedLocation"
        return parsed_data


# def total(location='aus', data_type='cases'):
#     print(location)

# print(new(data_type='recoveries', location='nsw'))
