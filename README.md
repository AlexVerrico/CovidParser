# CovidParser
## Adding the library to your project:
Using git: `git submodule add https://github.com/AlexVerrico/CovidParser.git && git submodule update --remote`  
Without git: download the zip from https://github.com/AlexVerrico/CovidParser/archive/1.0.0.zip and extract it into your project directory.
## Usage:
Import the module using `import CovidParser.covid_parser as covid`  
  
    
Available functions:
 - `covid.new(location="location", data_type="data type")`
   - Returns a list containing the requested data from the last 2 days, with the most recent data been first, eg `[5, 10]`.  
     `data_type` can be any one of: recoveries, deaths, cases  
     `location` can be any Australian state (using the common abrieviations, eg. vic for Victoria, nt for Northern Territory) or any other country supported by https://epidemic-stats.com/.

## Contributing:
If you find a bug to fix, or want to add a feature, please open an issue to discuss it first to avoid multiple people working on the same thing needlessly.  
Please ensure that all PRs are made to the `dev` branch  
Please ensure that you follow the style of the code (eg. spaces not tabs, function names use underscores, global variables use uppercase letters to seperate words (globalVariable), local variables are all lowercase with no seperation between words (localvariable)  
Please use descriptive function and variable names  
Please update any relevant documentation  

## Changelog:
 - V1.0.0 - First stable release

## Contributors:
 - [@AlexVerrico](https://github.com/AlexVerrico/)
