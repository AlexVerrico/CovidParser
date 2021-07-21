import __init__ as CovidParser

if __name__ == '__main__':
    covid = CovidParser.CovidParser(cache_type=1, cache_update_interval=3)
    do_continue = True
    while do_continue is True:
        _location = input('location: ')
        if _location == '!exit':
            do_continue = False
            continue
        _data_type = input('data type: ')
        _date_range = {}
        _temp = input('date_range: ').split(':')
        _date_range['type'] = _temp[0]
        _date_range['value'] = int(_temp[1])
        _type = input('new or total: ')
        if _type == 'new':
            _include_date = input('Include date [y] [n]: ')
            if _include_date == 'y':
                _include_date = True
            else:
                _include_date = False
            print(covid.new(location=_location, data_type=_data_type, date_range=_date_range, include_date=_include_date))
        elif _type == 'total':
            print(covid.total(location=_location, data_type=_data_type, date_range=_date_range))
    exit(0)
