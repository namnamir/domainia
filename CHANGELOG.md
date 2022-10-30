# Change Log
All notable changes to **Domainia** project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [2.0.1] - 2022-10-30
### Fixed
- The version number was fixed.

## [2.0.0] - 2022-10-30
### Fixed
- N/A

### Changed
- Improve the print format of graph lines.
- Change the name of the file `basic_status.py` to `html_status.py`.
- Fix issues of the code based on [CodeFactor suggestions](https://www.codefactor.io/repository/github/namnamir/domainia/issues).
- Make the function in `html_status.py` better in formatting and logic.
- Reformat the `config.py` file to make it more readable.

### Added
- Add disclaimer.
- Add the IP geo-location and ASN ([#3](https://github.com/namnamir/domainia/issues/3)).
- Add the random User Agent to the HTTP requests ([#24](https://github.com/namnamir/domainia/issues/24)).
- Add the delay between loading domains, DNS queries, and downloading SSL certificates ([#1](https://github.com/namnamir/domainia/issues/1)).
- Add DNSSec validation ([#7](https://github.com/namnamir/domainia/issues/7)).
- Add DKIM, SPF, and DMARC validator ([#10](https://github.com/namnamir/domainia/issues/10)).
- Add the Hacker Target API for subdomain enumeration ([#30](https://github.com/namnamir/domainia/issues/30)).
- Add a list of DKIM default selectors to the `config.py` file.
- Add a new module for subdomain finding.
- Add SSLMate (CertPotter) API to parse SSL ([#8](https://github.com/namnamir/domainia/issues/8)).
- Add a function to `utils.py` that sanitizes domain names before starting the analysis ([#35](https://github.com/namnamir/domainia/issues/35)).
- Add a set to check if the domain is already analyzed to prevent repetition ([#34](https://github.com/namnamir/domainia/issues/34)).
- Add a function to check the domain name and find it in the given text.
- Add more data from parsing the HTML file: Google UA ID, robots, Twitter, account ([#33](https://github.com/namnamir/domainia/issues/33)).
- Add a file `output_csv.py` to separate the CSV writer.
- The console output (STDOUT) will be saved into a `.txt` file ([#39](https://github.com/namnamir/domainia/issues/39)).
- The console output (STDOUT) verbosity can be set by the argument `-v` or `--verbosity` in 5 levels ([#38](https://github.com/namnamir/domainia/issues/38)).
- Add the error handling in exporting to CSV.
- The output would be written in a JSON file too ([#40](https://github.com/namnamir/domainia/issues/40)).

### Removed
- Remove subdomain and related domain sections of `ssl_parser.py` and add to the `subdomain_finder.py` module.

----

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
