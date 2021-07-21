# Copyright (C) 2021 Alex Verrico (https://alexverrico.com/). All Rights Reserved.
# Australian covid statistics are provided by https://covid19data.com.au/
# International covid statistics are provided by https://epidemic-stats.com/
# Docs at https://github.com/AlexVerrico/CovidParser

import json  # Used for loading and exporting data
import urllib.request  # Used to fetch data
from time import time  # Used for the caching system
from re import search as re_search, DOTALL  # Used for parsing data from epidemic-stats
from typing import TypedDict  # Used for declaring a custom return type for functions

# Standard output format used by all public functions of CovidParser
StandardReturnTypeV3 = TypedDict('StandardReturnTypeV3', {'status': str, 'content': str, 'classified': int})
# Required format for any CovidParser functions with the 'date_range' argument
DateRangeTypeV3 = TypedDict('DateRangeTypeV3', {'type': str, 'value': str})


class CovidParser:
    def __init__(self, cache_type=0, cache_update_interval=0, log_file=None):
        # Set the cache type, with a default to fallback to
        try:
            self.cache_type = int(cache_type)
        except ValueError:
            self.cache_type = 0
        # Set the cache update interval, with a default to fallback to
        try:
            self.cache_update_interval = int(cache_update_interval)
        except ValueError:
            self.cache_update_interval = 5

        # Set the self.print variable to point to the correct function
        if log_file is None:
            self.print = print
        else:
            self.print = self.__log
            # Store the log file location
            self.log_file = log_file

        # Dictionary to store cached data in with an example entry
        self.data_cache_v3 = {
            'example': {  # URL
                'timestamp': int(str(time()).split('.')[0]),  # Timestamp of when it was last downloaded
                'uses': 0,  # Number of uses since it was last downloaded
                'data': 'json data'  # Data
            }
        }

        # Dictionary of locations, their appropriate functions, and various other data
        self.__locations_v3 = {'aus': {'new_function': self.__get_aus_new_v3},
                               'nsw': {
                                   # Function to call for per day new cases|deaths|recoveries
                                   'new_function': self.__get_state_new_v3,
                                   'new_cases_index': 1,  # Index required for part of __get_state_new_v3
                                   'new_deaths_index': 1,  # Index required for part of __get_state_new_v3
                                   'new_recoveries_index': 1  # Index required for part of __get_state_new_v3
                               },
                               'vic': {'new_function': self.__get_state_new_v3,
                                       'new_cases_index': 2,
                                       'new_deaths_index': 2,
                                       'new_recoveries_index': 2},
                               'qld': {'new_function': self.__get_state_new_v3,
                                       'new_cases_index': 3,
                                       'new_deaths_index': 3,
                                       'new_recoveries_index': 3},
                               'sa': {'new_function': self.__get_state_new_v3,
                                      'new_cases_index': 4,
                                      'new_deaths_index': 4,
                                      'new_recoveries_index': 4},
                               'wa': {'new_function': self.__get_state_new_v3,
                                      'new_cases_index': 5,
                                      'new_deaths_index': 5,
                                      'new_recoveries_index': 5},
                               'tas': {'new_function': self.__get_state_new_v3,
                                       'new_cases_index': 6,
                                       'new_deaths_index': 6,
                                       'new_recoveries_index': 6},
                               'nt': {'new_function': self.__get_state_new_v3,
                                      'new_cases_index': 7,
                                      'new_deaths_index': 7,
                                      'new_recoveries_index': 7},
                               'act': {'new_function': self.__get_state_new_v3,
                                       'new_cases_index': 8,
                                       'new_deaths_index': 8,
                                       'new_recoveries_index': 8}
                               }

        # Mapping of long/full location names to their corresponding names in self.__locations_v3
        self.__locations_long_v3 = {'australia': 'aus',
                                    'new south wales': 'nsw',
                                    'victoria': 'vic',
                                    'queensland': 'qld',
                                    'south australia': 'sa',
                                    'western australia': 'wa',
                                    'tasmania': 'tas',
                                    'northern territory': 'nt',
                                    'australian capital territory': 'act',
                                    'america': 'usa'
                                    }
        return

    # Basic function to append output to a file
    def __log(self, data):
        # Open the file in append mode
        with open(self.log_file, 'a') as f:
            # Write the data
            f.write(data)
        return

    # Function to replace X number of occurences of a string with
    # a different string, starting at the end of the input string
    def __rreplace(self, s, old, _new, occurrence):
        li = s.rsplit(old, occurrence)
        return _new.join(li)

    # Function to store the data for a URL in the cache and set uses and timestamp for the entry
    def __update_cache_v3(self, url):
        # Check if the URL is cached, and if not create an empty entry in the cache
        try:
            self.data_cache_v3[url]
        except KeyError:
            self.data_cache_v3[url] = {}
        # Set the uses to 0 and the timestamp to the current time for the entry in the cache
        self.data_cache_v3[url]['uses'] = 0
        self.data_cache_v3[url]['timestamp'] = int(str(time()).split('.')[0])
        # Fetch the url and store the response in the cache
        with urllib.request.urlopen(url) as response:
            self.data_cache_v3[url]['data'] = response.read().decode('utf-8')
        # Return the updated data
        return self.data_cache_v3[url]['data']

    # Function to check whether an entry in the cache needs to be updated
    # If it does, it will update it then return the data, otherwise it will return the cached data
    def __download_data_v3(self, url):
        # Check if the URL is in the cache
        if url in self.data_cache_v3:
            # If the we aren't truly caching the URL, then update the cache and return the result
            if self.cache_type == 0:
                return self.__update_cache_v3(url)
            # If we are caching based on number of uses
            elif self.cache_type == 1:
                # Check if the cache needs to be updated, and return the appropriate data
                if self.data_cache_v3[url]['uses'] >= self.cache_update_interval:
                    return self.__update_cache_v3(url)
                else:
                    self.data_cache_v3[url]['uses'] = self.data_cache_v3[url]['uses'] + 1
                    return self.data_cache_v3[url]['data']
            # If we are caching based on time since last update
            elif self.cache_type == 2:
                # Check if the cache needs to be updated, and return the appropriate data
                if (int(str(time()).split('.')[0]) - self.data_cache_v3[url]['timestamp']) > self.cache_update_interval:
                    return self.__update_cache_v3(url)
                else:
                    self.data_cache_v3[url]['uses'] = self.data_cache_v3[url]['uses'] + 1
                    return self.data_cache_v3[url]['data']
        # If the URL isn't in the cache, then we return the output of __update_cache_v3
        else:
            return self.__update_cache_v3(url)

    # Function to retrieve and parse data for any Australian state
    def __get_state_new_v3(self, data_type: str = 'cases', date_range: DateRangeTypeV3 = None,
                           include_date: bool = False, location: str = 'vic') -> StandardReturnTypeV3:
        # Default date range
        if date_range is None:
            date_range = {'type': 'days', 'value': 2}

        # Default output
        out_full = {
            'status': 'ok',
            'content': '',
            'classified': 0
        }

        # Function to avoid repeating code
        def __get_state_new_v3_iter_func(_data: list, _range_top: int, _index: int, _include_date: bool) -> list:
            # Initialize output list
            output = []
            # If the call requested more values that what are available, return the maximum available
            if _range_top > len(_data) - 1:
                _range_top = len(_data) - 1
            # Initialise variables to store where we are up to in the data, and how many valid outputs we have
            current_pos = 0
            num_results = 0
            # While we don't have the requested amount of output
            while num_results < _range_top:
                # If the current entry in the input is empty, then we skip it
                if _data[int('-{}'.format(str(current_pos + 1)))][0] == "" or \
                        _data[int('-{}'.format(str(current_pos + 1)))][0] == " ":
                    current_pos = current_pos + 1
                    continue
                num_results = num_results + 1
                # Append the correct data format to the output, depending on the value of _include_data
                if _include_date is True:
                    output.append([_data[int('-{}'.format(str(current_pos + 1)))][0],
                                   _data[int('-{}'.format(str(current_pos + 1)))][_index]])
                else:
                    output.append(_data[int('-{}'.format(str(current_pos + 1)))][_index])
                current_pos = current_pos + 1
            # Return the output
            return output

        # If the requested data_type is cases
        if data_type == 'cases':
            # Get the correct data and load it
            data = self.__download_data_v3(r'https://atlas.jifo.co/api/connectors/0b334273-5661-4837-a639-e3a384d81d20')
            data = json.loads(data)['data'][7]
            # If the date_range is in days, call __get_state_new_v3_iter_func
            if date_range['type'] == 'days':
                out = __get_state_new_v3_iter_func(data, date_range['value'],
                                                   self.__locations_v3[location]['new_cases_index'], include_date)
            # If the date_range is all, then reverse the entire input and return it
            elif date_range['type'] == 'all':
                out = []
                for i in range(0, len(data) - 1):
                    # If the current entry in the input is empty, then we skip it
                    if data[int('-{}'.format(str(i + 1)))][0] == "" or \
                            data[int('-{}'.format(str(i + 1)))][0] == " ":
                        continue
                    # Append the correct data format to the output, depending on the value of _include_data
                    if include_date is True:
                        out.append([data[int('-{}'.format(str(i + 1)))][0],
                                    data[int('-{}'.format(str(i + 1)))][
                                        self.__locations_v3[location]['new_cases_index']]])
                    else:
                        out.append(
                            data[int('-{}'.format(str(i + 1)))][self.__locations_v3[location]['new_cases_index']])
            else:
                # If the date_range was invalid, log and return an error
                self.print(f"Unsupported date_range type in CovidParser.__get_state_new_v3(date_range={date_range})")
                out_full['status'] = 'error'
                out_full['content'] = 'Unsupported date_range'
                return out_full
            # Return the output in JSON format
            out_full['content'] = json.dumps(out)
            return out_full

        elif data_type == 'deaths':
            data = self.__download_data_v3(r'https://atlas.jifo.co/api/connectors/0b334273-5661-4837-a639-e3a384d81d20')
            data = json.loads(data)['data'][16]
            if date_range['type'] == 'days':
                out = __get_state_new_v3_iter_func(data, date_range['value'],
                                                   self.__locations_v3[location]['new_deaths_index'], include_date)
            elif date_range['type'] == 'all':
                out = []
                for i in range(0, len(data) - 1):
                    # If the current entry in the input is empty, then we skip it
                    if data[int('-{}'.format(str(i + 1)))][0] == "" or \
                            data[int('-{}'.format(str(i + 1)))][0] == " ":
                        continue
                    if include_date is True:
                        out.append([data[int('-{}'.format(str(i + 1)))][0],
                                    data[int('-{}'.format(str(i + 1)))][
                                        self.__locations_v3[location]['new_deaths_index']]]
                                   )
                    else:
                        out.append(
                            data[int('-{}'.format(str(i + 1)))][self.__locations_v3[location]['new_deaths_index']])
            else:
                self.print(f"Unsupported date_range type in CovidParser.__get_state_new_v3(date_range={date_range})")
                out_full['status'] = 'error'
                out_full['content'] = 'Unsupported date_range'
                return out_full
            out_full['content'] = json.dumps(out)
            return out_full

        # If the data_type is recoveries
        elif data_type == 'recoveries':
            out = []
            # Get the correct data and load it
            data = self.__download_data_v3(r'https://atlas.jifo.co/api/connectors/1806e38a-75e1-44b3-a9ed-fb384165cabf')
            data = json.loads(data)['data']
            # If the call requested more values that what are available, return the maximum available
            if date_range['type'] == 'days':
                if date_range['value'] > len(data[self.__locations_v3[location]['new_recoveries_index']]) - 1:
                    date_range['value'] = len(data[self.__locations_v3[location]['new_recoveries_index']]) - 2
                i = 0
                x = 0
                # While we don't have the requested amount of output
                while x < date_range['value']:
                    # If the current entry in the input is empty, then we skip it
                    if data[int('-{}'.format(str(i + 1)))][0] == "" or data[int('-{}'.format(str(i + 1)))][0] == " ":
                        i = i + 1
                        continue
                    x = x + 1
                    # Append the correct data format to the output, depending on the value of _include_data
                    if include_date is True:
                        # This part is a little more complicated for recoveries than it is for cases or deaths
                        try:
                            out.append(
                                # Date
                                [data[self.__locations_v3[location]['new_recoveries_index']][
                                     int('-{}'.format(str(i + 1)))][0],
                                 # Total recoveries in the current entry
                                 str(int(data[self.__locations_v3[location]['new_recoveries_index']][
                                             int('-{}'.format(str(i + 1)))][3]) -
                                     # Minus the previous entry (one closer to the start of the input)
                                     int(data[self.__locations_v3[location]['new_recoveries_index']][
                                             int('-{}'.format(str(i + 2)))][3]))])
                        except ValueError:
                            self.print("valueError")
                            out.append([
                                data[self.__locations_v3[location]['new_recoveries_index']][
                                    int('-{}'.format(str(i + 1)))][
                                    0], ''])
                    else:
                        try:
                            out.append(
                                str(int(data[self.__locations_v3[location]['new_recoveries_index']][
                                            int('-{}'.format(str(i + 1)))][3]) -
                                    int(data[self.__locations_v3[location]['new_recoveries_index']][
                                            int('-{}'.format(str(i + 2)))][3])))
                        except ValueError:
                            self.print("valueError")
                            out.append('')
                    i = i + 1
            # If the date_range is all, then reverse the entire input and return it
            elif date_range['type'] == 'all':
                for i in range(0, len(data[self.__locations_v3[location]['new_recoveries_index']]) - 2):
                    if include_date is True:
                        try:
                            out.append([
                                data[self.__locations_v3[location]['new_recoveries_index']][
                                    int('-{}'.format(str(i + 1)))][
                                    0],
                                str(int(data[self.__locations_v3[location]['new_recoveries_index']][
                                            int('-{}'.format(str(i + 1)))][3]) -
                                    int(data[self.__locations_v3[location]['new_recoveries_index']][
                                            int('-{}'.format(str(i + 2)))][3]))])
                        except ValueError:
                            self.print("valueError")
                            out.append([
                                data[self.__locations_v3[location]['new_recoveries_index']][
                                    int('-{}'.format(str(i + 1)))][
                                    0], ''])
                    else:
                        try:
                            out.append(
                                str(int(data[self.__locations_v3[location]['new_recoveries_index']][
                                            int('-{}'.format(str(i + 1)))][3]) -
                                    int(data[self.__locations_v3[location]['new_recoveries_index']][
                                            int('-{}'.format(str(i + 2)))][3])))
                        except ValueError:
                            self.print("valueError")
                            out.append('')
            else:
                self.print(f"Unsupported date_range type in CovidParser.__get_state_new_v3(date_range={date_range})")
                out_full['status'] = 'error'
                out_full['content'] = 'Unsupported date_range'
                return out_full
            out_full['content'] = json.dumps(out)
            return out_full

        # If the data_type isn't cases, deaths, or recoveries, log and return an error
        else:
            self.print(f"Unsupported data_type type in CovidParser.__get_state_new_v3(data_type={data_type})")
            out_full['status'] = 'error'
            out_full['content'] = 'Unsupported data_type'
            return out_full

    def __get_aus_new_v3(self, data_type: str = 'cases', date_range: DateRangeTypeV3 = None,
                         include_date: bool = False, location: str = 'aus') -> StandardReturnTypeV3:
        if date_range is None:
            date_range = {'type': 'days', 'value': 2}
        out_full = {
            'status': 'ok',
            'content': '',
            'classified': 0
        }
        if data_type == 'cases':
            out = []
            data = self.__download_data_v3(r'https://atlas.jifo.co/api/connectors/0b334273-5661-4837-a639-e3a384d81d20')
            data = json.loads(data)['data']
            if date_range['type'] == 'days':
                if date_range['value'] > len(data[3]) - 1:
                    date_range['value'] = len(data[3]) - 1
                data = data[3]
                i = 0
                x = 0
                while x < date_range['value']:
                    if data[int('-{}'.format(str(i + 1)))][0] == "" or data[int('-{}'.format(str(i + 1)))][0] == " ":
                        i = i + 1
                        continue
                    x = x + 1
                    if include_date is True:
                        out.append(data[int('-{}'.format(str(i + 1)))])
                    else:
                        out.append(data[int('-{}'.format(str(i + 1)))][1])
                    i = i + 1
            elif date_range['type'] == 'all':
                data = data[3]
                for i in range(0, len(data) - 1):
                    if data[int('-{}'.format(str(i + 1)))][0] == "" or data[int('-{}'.format(str(i + 1)))][0] == " ":
                        continue
                    if include_date is True:
                        out.append(data[int('-{}'.format(str(i + 1)))])
                    else:
                        out.append(data[int('-{}'.format(str(i + 1)))][1])
            else:
                self.print(f"Unsupported date_range type in CovidParser.__get_aus_new_v3(date_range={date_range})")
                out_full['status'] = 'error'
                out_full['content'] = 'Unsupported date_range'
                return out_full
            out_full['content'] = json.dumps(out)
            return out_full
        elif data_type == 'deaths':
            out = []
            data = self.__download_data_v3(r'https://atlas.jifo.co/api/connectors/0b334273-5661-4837-a639-e3a384d81d20')
            data = json.loads(data)['data']
            if date_range['type'] == 'days':
                if date_range['value'] > len(data[11]) - 1:
                    date_range['value'] = len(data[11]) - 1
                data = data[11]
                i = 0
                x = 0
                while x < date_range['value']:
                    if data[int('-{}'.format(str(i + 1)))][0] == "" or data[int('-{}'.format(str(i + 1)))][0] == " ":
                        i = i + 1
                        continue
                    x = x + 1
                    if include_date is True:
                        out.append(data[int('-{}'.format(str(i + 1)))])
                    else:
                        out.append(data[int('-{}'.format(str(i + 1)))][1])
                    i = i + 1
            elif date_range['type'] == 'all':
                data = data[11]
                for i in range(0, len(data) - 1):
                    if include_date is True:
                        out.append(data[int('-{}'.format(str(i + 1)))])
                    else:
                        out.append(data[int('-{}'.format(str(i + 1)))][1])
            else:
                self.print(f"Unsupported date_range type in CovidParser.__get_aus_new_v3(date_range={date_range})")
                out_full['status'] = 'error'
                out_full['content'] = 'Unsupported date_range'
                return out_full
            out_full['content'] = json.dumps(out)
            return out_full
        elif data_type == 'recoveries':
            out = []
            data = self.__download_data_v3(r'https://atlas.jifo.co/api/connectors/0b334273-5661-4837-a639-e3a384d81d20')
            data = json.loads(data)['data']
            data = data[43]
            if date_range['type'] == 'days':
                if date_range['value'] > len(data) - 1:
                    date_range['value'] = len(data) - 1
                i = 0
                x = 0
                while x < date_range['value']:
                    if data[int('-{}'.format(str(i + 1)))][0] == "" or data[int('-{}'.format(str(i + 1)))][0] == " ":
                        i = i + 1
                        continue
                    x = x + 1
                    if include_date is True:
                        out.append([data[int('-{}'.format(str(i + 1)))][0], data[int('-{}'.format(str(i + 1)))][5]])
                    else:
                        out.append(data[int('-{}'.format(str(i + 1)))][5])
                    i = i + 1
            elif date_range['type'] == 'all':
                for i in range(0, len(data) - 1):
                    if include_date is True:
                        out.append([data[int('-{}'.format(str(i + 1)))][0], data[int('-{}'.format(str(i + 1)))]][5])
                    else:
                        out.append(data[int('-{}'.format(str(i + 1)))][5])
            else:
                self.print(f"Unsupported date_range type in CovidParser.__get_aus_new_v3(date_range={date_range})")
                out_full['status'] = 'error'
                out_full['content'] = 'Unsupported date_range'
                return out_full
            out_full['content'] = json.dumps(out)
            return out_full
        else:
            self.print(f"Unsupported data_type in CovidParser.__get_aus_new_v3(data_type={data_type})")
            out_full['status'] = 'error'
            out_full['content'] = 'Unsupported data_type'
            return out_full

    def __get_country_new_v3(self, data_type: str = 'cases', date_range: DateRangeTypeV3 = None,
                             include_date: bool = False, location: str = 'australia') -> StandardReturnTypeV3:
        if date_range is None:
            date_range = {'type': 'days', 'value': 2}
        data = self.__download_data_v3(r'https://epidemic-stats.com/coronavirus/{country}'
                                       .format(country=location.lower()))
        out_full = {
            'status': 'ok',
            'content': '',
            'classified': 0
        }
        if data_type == 'cases':
            regex = ".+const infected_new = (.+)const recovered_new = .+"
            data = json.loads(self.__rreplace(re_search(regex, data, DOTALL)[1].replace("'", '"'), ',', '', 1))
        elif data_type == 'deaths':
            regex = ".+const deaths_new = (.+)const infected_new = .+"
            data = json.loads(self.__rreplace(re_search(regex, data, DOTALL)[1].replace("'", '"'), ',', '', 1))
        elif data_type == 'recoveries':
            regex = ".+const recovered_new = (.+)const current_infected = .+"
            data = json.loads(self.__rreplace(re_search(regex, data, DOTALL)[1].replace("'", '"'), ',', '', 1))
        else:
            self.print(f"Unsupported data_type in CovidParser.__get_country_new_v3(data_type={data_type}")
            out_full['status'] = 'error'
            out_full['content'] = 'Unsupported data_type'
            return out_full
        out = []
        if date_range['type'] == 'days':
            if date_range['value'] > len(data):
                date_range['value'] = len(data)
            for i in range(0, date_range['value']):
                out.append(data[-i])
        elif date_range['type'] == 'all':
            for i in range(0, len(data)):
                out.append(data[-i])
        else:
            self.print(f"Unsupported date_range type in CovidParser.__get_country_new_v3(date_range={date_range})")
            out_full['status'] = 'error'
            out_full['content'] = 'Unsupported date_range'
            return out_full
        out_full['content'] = json.dumps(out)
        return out_full

    def _new_v3(self, location: str = 'aus', data_type: str = 'cases', date_range: DateRangeTypeV3 = None,
                include_date: bool = False) -> StandardReturnTypeV3:
        if date_range is None:
            date_range = {'type': 'days', 'value': 2}
        out_full = {
            'status': 'ok',
            'content': '',
            'classified': 0
        }
        if location in self.__locations_long_v3:
            location = self.__locations_long_v3[location]
        if location in self.__locations_v3:
            out = self.__locations_v3[location]['new_function'](
                data_type=data_type, date_range=date_range, include_date=include_date, location=location)
            if out['classified'] == 0:
                return out
            elif out['classified'] == 1:
                self.print(out)
                out_full['status'] = 'error'
                out_full['content'] = 'See logs'
                return out_full
            else:
                out_full['status'] = 'error'
                out_full['content'] = 'Not logged, check exceptions'
                return out_full

        else:
            try:
                out = self.__get_country_new_v3(location=location, data_type=data_type)
                if out['classified'] == 0:
                    return out
                elif out['classified'] == 1:
                    self.print(out)
                    out_full['status'] = 'error'
                    out_full['content'] = 'Error: See logs'
                    return out_full
                else:
                    out_full['status'] = 'error'
                    out_full['content'] = 'Error: not logged, level >= 2'
                    return out_full
            except urllib.error.HTTPError:
                out_full['status'] = 'error'
                out_full['content'] = "Unrecognised location"
                out_full['classified'] = 0
                return out_full

    def _total_v3(self, location: str = 'aus', data_type: str = 'cases',
                  date_range: DateRangeTypeV3 = None) -> StandardReturnTypeV3:
        if date_range is None:
            date_range = {'type': 'all', 'value': 2}
        out_full = {
            'status': 'ok',
            'content': '',
            'classified': 0
        }
        if location in self.__locations_long_v3:
            location = self.__locations_long_v3[location]
        if location in self.__locations_v3:
            out = self.__locations_v3[location]['new_function'](
                data_type=data_type, date_range=date_range, include_date=False, location=location)

            if out['classified'] == 1:
                self.print(out)
                out_full['status'] = 'error'
                out_full['content'] = 'See logs'
                return out_full
            elif out['classified'] >= 2:
                out_full['status'] = 'error'
                out_full['content'] = 'Not logged, check exceptions'
                return out_full

            total = 0

            for i in json.loads(out['content']):
                try:
                    int(i)
                except ValueError:
                    continue
                total = total + int(i)

            out_full['content'] = total
            return out_full

        else:
            try:
                out = self.__get_country_new_v3(
                    location=location, data_type=data_type, date_range=date_range, include_date=False, )

                if out['classified'] == 1:
                    self.print(out)
                    out_full['status'] = 'error'
                    out_full['content'] = 'Error: See logs'
                    return out_full
                elif out['classified'] >= 2:
                    out_full['status'] = 'error'
                    out_full['content'] = 'Error: not logged, level >= 2'
                    return out_full

                total = 0

                for i in json.loads(out['content']):
                    try:
                        total = total + int(i)
                    except ValueError:
                        total = total + 0

                out_full['content'] = total
                return out_full

            except urllib.error.HTTPError:
                out_full['status'] = 'error'
                out_full['content'] = "Unrecognised location"
                out_full['classified'] = 0
                return out_full

    def new(self, location: str = 'aus', data_type: str = 'cases',
            date_range: DateRangeTypeV3 = None, include_date: bool = False) -> StandardReturnTypeV3:
        return self._new_v3(location=location.lower(), data_type=data_type.lower(),
                            date_range=date_range, include_date=include_date)

    def total(self, location: str = 'aus', data_type: str = 'cases',
              date_range: DateRangeTypeV3 = None) -> StandardReturnTypeV3:
        return self._total_v3(location=location.lower(), data_type=data_type.lower(), date_range=date_range)
