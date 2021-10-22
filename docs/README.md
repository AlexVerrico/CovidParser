# Module reference

### Adding the module to your project: 

`git submodule add https://github.com/AlexVerrico/CovidParser.git && git submodule update --remote`

### Importing the module:

```
import CovidParser
```

### Creating a CovidParser object to use:

With default options: 
```python
covid = CovidParser.CovidParser()
```  

Available options:

- `cache_type`
    - The caching method to use. Can be  
      0 for no caching,   
      1 to cache each URL for `cache_update_interval` number of uses, or   
      2 to cache each URL for `cache_update_interval` number of seconds.
- `cache_update_interval`
    - Used in conjunction with `cache_type`.
- `log_file`
    - File to log to. If set to `None` (default), then the module will log to the standard terminal output (using `print()`)
    
For example, to create an object which refreshes the data every 3 calls, and logs to `/var/log/CovidParser.txt`:
```python
covid = CovidParser.CovidParser(cache_type=1, cache_update_interval=3, log_file='/var/log/CovidParser.txt')
```

### Using the CovidParser object:
 
```python
# Fetch a list of new cases, per day, since the start of the dataset for Victoria, and don't include the date of each entry in the output:
data = covid.new(location='vic', data_type='cases', date_range={'type': 'all'}, include_date=False)
# Returns {'status': 'ok', 'content': '["23", "15", "14", ... "0", "1", "0"]', 'classified': 0}

# Fetch total confirmed cases since the start of the dataset for Victoria:  
data = covid.total(location='vic', data_type='cases', date_range={'type': 'all'})
# Returns {'status': 'ok', 'content': 20837, 'classified': 0}

# Fetch a list of new cases, per day, for the last 2 days in Victoria, and include the date with each entry:
data = covid.new(location='vic', data_type='cases', date_range={'type': 'days', 'value': 30}, include_date=True)
# Returns {'status': 'ok', 'content': '[["21/07/21", "23"], ["20/07/21", "15"]]', 'classified': 0}
```

All functions return a standard output format:
```python
{
    'status': 'ok',
    'content': '<content>',
    'classified': 0
}
```

`status` will normally be `ok`, however if something goes wrong then it will be `error`.  
`content` will contain the actual output from the function (or a more detailed error message of `status` is `error`).  
`classified` denotes whether the content of the response is suitable to be passed along to the user.  
0 means ok to return to user, 1 means that the data is ok to log but shouldn't be returned to the user, 2 means that the data shouldn't be logged but can be included in any exceptions raised, 3 or higher means that the data shouldn't be returned to the user, logged, or included in any exceptions.  
Normally, any data returned by the module will have a `classified` value of 0, however if you choose to use the underlying methods then you need to check this yourself.


0 = ok to return to user  
1 = not to be returned to user  
2 = not to be returned to user, not to be logged  
3 = not to be returned to user, not to be logged, not to be raised in exceptions  

Available data_types:
- Cases
- Deaths
- Recoveries
- Vaccinations (alias for vaccinations-seconddose)
- Vaccinations-seconddose
- Vaccinations-firstdose

The following locations have full support:
location (full name)
- aus (Australia)
- nsw (New South Wales)
- vic (Victoria)
- qld (Queensland)
- sa (South Australia)
- wa (Western Australia)
- tas (Tasmania)
- nt (Northern Territory)
- act (Australian Capital Territory)

Any locations that are supported by [https://epidemic-stats.com/coronavirus/country_name](https://epidemic-stats.com/coronavirus/country_name) can be used, with the following limitations:
- The option `include_date` for `CovidParser.new` will be ignored
- The data will always be returned without the date for each entry
- There is currently no support for vaccination data

It is also possible to access the underlying methods for some functions, however this bypasses any pre-processing, and so more care is required when passing arguments:  
`CovidParser._new_v3(location, data_type, date_range, include_date)`  
`CovidParser._total_v3(location, data_type, date_range)`  
These methods should only be used if you have an auto-update mechanism in place, and need to be sure that the output format will remain the same  
