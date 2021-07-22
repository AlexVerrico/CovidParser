# CovidParser

This module provides a way to retrieve and parse data from `covid19data.com.au` and `epidemic-stats.com/coronavirus/country_name`.  
See [docs/README.md](https://github.com/AlexVerrico/CovidParser/blob/master/docs/README.md) for more details.  

## Usage:
See [docs/README.md](https://github.com/AlexVerrico/CovidParser/blob/master/docs/README.md)

## Contributing:
If you find a bug to fix, or want to add a feature, please open an issue to discuss it first to avoid multiple people working on the same thing needlessly.  
Please ensure that all PRs are made to the `dev` branch  
Please ensure that you follow the style of the code  
Please use descriptive function and variable names  
Please update any relevant documentation  

## Changelog:

 - V1.0.0 - First stable release-
 - V2.0.0 - *If you're wondering where version 2 is, it never made it onto GitHub, but I still named the latest release version 3 to avoid conflicts where version 2 was deployed manually.*
 - V3.0.0 - Major overhaul, also adds CovidParser.total   
   ***Warning: This is not a "drop-in" replacement for V1.0.0.***
 - V3.0.1 - Add newline to `CovidParser.__log()`, and add `CovidParser._fetch_data_v3()` function.
 - V3.0.2 - Fix `CovidParser._new_v3()` to correctly pass date_range to `CovidParser.__get_country_new_v3()`

## Contributors:
 - [@AlexVerrico](https://github.com/AlexVerrico/)
