# Change Log
All notable changes to **Domainia** project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [1.2.0] - 2022-09-22
### Fixed
- N/A

### Changed
- Change the `url1` and `url2` in the `config.py` to be more understandable.
- Change the relative links in `README.md` to absolute ones.
- Remove the last `newline` from `whois.py` and add it to `__init.py`.
- Clean up the codes in `whois.py` and `ssl_parser.py`.
- Change the text of some error messages.
- Make the print of the results in the STDOut more readable.

### Added
- Add IP Whois ([#3](https://github.com/namnamir/domainia/issues/3)).
- Add more exceptions to `whois.py` and `ssl_parser.py` to handle more errors.
- Add the font to the repository.

### Removed
- N/A

## [1.1.0] - 2022-09-17
### Fixed
- Fix the situation when the API key is not set.
- Fix the issue of showing empty results when the API call is not made.

### Changed
- Change `init.py` to `__init.py` to make it compiled with PyPi guidelines.
- Change the `README.md` with more useful text.
- Make the `ssl_parser.py` cleaner.
- Change the logo and social preview ([#17](https://github.com/namnamir/domainia/issues/17)).

### Added
- Add `CHANGELOG.md` to log versions in a human readable format.
- Add `.gitignore` to ignore pushing some files to Github.
- Add `setup.py` to make the package ready uploaded to PyPi.
- Add the page [domainia.irsec.eu](https://domainia.irsec.eu).
- Add `*.csv` to `.gitignore` except the sample one.
- Add the color plate: `#323232`, `#c32266`, and `#4c4b4b` for logo and future designs.

### Removed
- All previous commits were deleted as mistakenly the API keys were publicized.
- Remove `.travis.yml` as it was not used.


## [1.0.0] - 2022-10-07
The project was abandoned for about a year. It's revived and some changes are 
made. Let's see it as te initial version, 1.0.0.
