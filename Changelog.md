# 1.4.1 - 2020-06-30
## Added
- Added validator for configuration file
## Changed
- Configurator module completely refactored
## Fixed
- Initial config file setup was broken, now creates the file in the right place


# 1.4.0 - 2020-06-28
## Added
- Query command
- Add from file command
- Associate command
## Fixed
- Minor logic errors spread throughout the code
## Changed
- Open command now recurssively search a direectory for files that contains, in their name, the isbn of one of the books that match the given query criteria

# 1.3.0 - 2020-06-21
## Added
- Path attribute to book model

# 1.2.0 - 2020-06-20
## Added
- extra_attrs configuration directive: user can not choose custom attributes for model
## Fixed
- fixed broken test

# 1.1.0 - 2020-06-20
## Added
- api_key_file configuration directive
- migration command
## Fixed
- configurator not turning string into path
