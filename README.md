[![PyPI](https://img.shields.io/pypi/v/domainia?style=flat-square)](https://pypi.org/project/Domainia/) ![GitHub last commit](https://img.shields.io/github/last-commit/namnamir/domainia?style=flat-square) [![GitHub issues](https://img.shields.io/github/issues-raw/namnamir/domainia?style=flat-square)](https://github.com/namnamir/domainia/issues) ![GitHub branch checks state](https://img.shields.io/github/checks-status/namnamir/domainia/main?style=flat-square) [![License](https://img.shields.io/github/license/namnamir/domainia?style=flat-square)](LICENSE)

<img src="https://raw.githubusercontent.com/namnamir/domainia/main/img/logo.png" width="150px" align="right">

**Domainia** Scanner is an automated Open-source Intelligence (OSINT) tool that enumerates subdomains, all DNS records, IP addresses, related domains/subdomains, certificate details, site info, HTTP status, name servers (NS), domain whois, and etc. of a single domain or a list of domains by using the passive and active reconnaissance techniques.

❤ Support Domainia: ![GitHub Sponsors](https://img.shields.io/github/sponsors/namnamir?style=flat-square) [![Liberapay patrons](https://img.shields.io/liberapay/patrons/namnamir?style=flat-square)](https://liberapay.com/namnamir/donate)

<img src="https://raw.githubusercontent.com/namnamir/domainia/main/img/logo2.png">

---
# How to Use
If you look for the changelog history, you can find it [here](https://github.com/namnamir/domainia/blob/main/CHANGELOG.md).

## 1. Installation
### 1.1. Installation Through [PyPi](https://pypi.org/project/Domainia/) 
[![PyPI](https://img.shields.io/pypi/v/domainia?style=flat-square)](https://pypi.org/project/Domainia/)

If you would like to install it as a Python package, run the following command.
```bash
pip install Domainia
# or
python -m pip install Domainia
```
### 1.2. Installation form the Source
First, clone the package from Github.
```bash
git clone https://github.com/namnamir/domainia.git
```
Then, by running the following command, install all required dependencies for the current user.
```Bash
pip install requirements.txt --user
```

## 2. Add API Keys
Modify the file `api_keys.py` and add the API keys of the mentioned tools.
![Define APIs](https://raw.githubusercontent.com/namnamir/domainia/main/img/api.png)

## 3. Check the Configuration File
Open the file `config.py` and modify it if needed. For each section of it, there is an explanation as the comment.

There are many options can be modified in the config file. Here are a list of the options:
- `date_format` to set the data and time format
- `scan_type` to set the scan type
- `dns_records` to set which DNS records should be enumerated
- `include_txt_records` to set which TXT records should be written in the output file
- `dns_servers` to set the DNS servers
- `delimiter` to set the delimiters for each data to be written into the CSV file
- `whois` to set which Whois detail should be written into the CSV file
- `ssl` to set which SSL detail should be written into the CSV file
- `api` to modify details of the APIs including the data/time format

## 4. Run the Script
The script can be run in 2 modes, loading the list of domains from a file or from the command.
```bash
  -h, --help
                        Show this help message and exit
  -f FILE, --file FILE  
                        Path to the list of domain names, e.g. domains.txt
  -d DOMAIN, --domain DOMAIN
                        The comma separated list of domains
  -w WHOIS, --whois WHOIS
                        Whois API; default "whoisxml".
                        Possible options: "whoisxml" and "whoxy"
-t TYPE, --type TYPE  
                       Type of the scan. If it is set, it will ignore the config file value for the scan type.
                       Possible options: "quick" and "deep"
  -o OUTPUT, --output OUTPUT
                        The name of the output CSV file, e.g. results.csv
```
![Run Domainia Scanner](https://raw.githubusercontent.com/namnamir/domainia/main/img/scan.gif)

## 5. Results (CSV)
Result of the scan would be saved in a CSV file. You can manage the path of the output file by the argument `-o` or `--output`.
![Results in CSV](https://raw.githubusercontent.com/namnamir/domainia/main/img/result.png)
![Results in CSV](https://raw.githubusercontent.com/namnamir/domainia/main/img/result2.png)

---
**Copyright**
- This tool is released under copy left; there is no right. Read more about it on the [LICENSE page](https://github.com/namnamir/domainia/blob/main/LICENSE).
