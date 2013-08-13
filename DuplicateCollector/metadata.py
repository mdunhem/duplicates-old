""":mod:`my_module.metadata` --- Project metadata

Information describing the project.
"""

# The package name, which is also the "UNIX name" for the project.
package = 'DuplicateCollector'
project = "Duplicate Files Collecting Tool"
project_no_spaces = project.replace(' ', '')
version = '0.1'
description = 'Scans through files in the provided directory and collects a list of binary duplicates, regardless of filename.'
authors = ['Mikael Dunhem']
authors_string = ', '.join(authors)
emails = ['mikael.dunhem@gmail.com']
license = 'MIT'
copyright = '2013 ' + authors_string
url = 'http://github.com/mdunhem/DuplicateCollector'
