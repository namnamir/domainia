[![PyPI](https://img.shields.io/pypi/v/domainia?style=flat-square)](https://pypi.org/project/domainia/) ![GitHub last commit](https://img.shields.io/github/last-commit/namnamir/domainia?style=flat-square) [![CodeFactor](https://www.codefactor.io/repository/github/namnamir/domainia/badge)](https://www.codefactor.io/repository/github/namnamir/domainia) [![GitHub issues](https://img.shields.io/github/issues-raw/namnamir/domainia?style=flat-square)](https://github.com/namnamir/domainia/issues) ![GitHub branch checks state](https://img.shields.io/github/checks-status/namnamir/domainia/main?style=flat-square) [![License](https://img.shields.io/github/license/namnamir/domainia?style=flat-square)](LICENSE)

<img src="https://raw.githubusercontent.com/namnamir/domainia/main/img/logo.png" width="150px" align="right">

**Domainia** Scanner is an automated Open-source Intelligence (OSINT) tool that enumerates subdomains, all DNS records, IP addresses, related domains/subdomains, certificate details, site info, HTTP status, name servers (NS), domain whois, and etc. of a single domain or a list of domains by using the passive and active reconnaissance techniques.

❤ Support Domainia: ![GitHub Sponsors](https://img.shields.io/github/sponsors/namnamir?style=flat-square) [![Liberapay patrons](https://img.shields.io/liberapay/patrons/namnamir?style=flat-square)](https://liberapay.com/namnamir/donate)

<img src="https://raw.githubusercontent.com/namnamir/domainia/main/img/logo2.png">

---
# How to Use
If you look for the changelog history, you can find it [here](https://github.com/namnamir/domainia/blob/main/CHANGELOG.md).

## 1. Installation
### 1.1. From PyPI
```bash
pip install domainia
# or using uv
uv pip install domainia
```

### 1.2. From Source
```bash
git clone https://github.com/namnamir/domainia.git
cd domainia

# using uv (recommended)
uv sync

# or with pip
python -m pip install -e .
```

## 2. Add API Keys
Modify the file `api_keys.py` and add the API keys of the mentioned tools.
![Define APIs](https://raw.githubusercontent.com/namnamir/domainia/main/img/api.png)

## 3. Check the Configuration File
Open the file `config.py` and modify it if needed. For each section of it, there is an explanation as the comment.

There are many powerful options in `config.py` to customize how Domainia works. You can:
- Enable or disable modules: scan HTTP, DNS, SSL/TLS, Whois, subdomains;
- Pick scan type: "quick" or "deep" (for faster or more comprehensive scans);
- Configure what DNS/TXT records to check and which SSL/HTTP metadata to collect (including fine-grained toggles);
- Set customizable timeouts and randomized per-domain delays;
- Change output format to TXT, JSON, YAML (**CSV output is currently disabled**);
- Adjust verbosity, output files, and much more.

API Keys: For services like WhoisXML, Whoxy, Shodan, and others, add your keys to the corresponding lists in `config.py`. **Domainia supports rotating through multiple keys at random per provider, reducing the chance of rate-limit blocks and maximizing scan coverage even on strict APIs.**

Advanced users can tweak almost every scan or output detail to suit unique OSINT, research, or automation needs. See detailed comments in `config.py` for more.

## 4. CLI Usage
You can run Domainia via the installed console script or directly:
```bash
domainia help
domainia version
domainia scan -i domains.txt -o results -F json -D 0

# or
python main.py help
python main.py scan -d example.com,example.org -o results
```

### Usage and Arguments
```
usage: Get the public information of a domain [-h] [-i INPUT] [-d DOMAIN] [-w {whoisxml,whoxy}] [-t {quick,deep}]
                                              [-o OUTPUT] [-s] [-D DELAY] [-F OUTPUT_FORMAT] [-v] [--version]

  -h, --help            show this help message and exit

  -i, --input INPUT     Path to the list of domain names, e.g. domains.txt. Each domain name should be in a line.
  -d, --domain DOMAIN   The comma separated list of domains
  -w, --whois {whoisxml,whoxy}
                        Whois API; default "whoisxml". Possible options: "whoisxml" and "whoxy"
  -t, --type {quick,deep}
                        Type of the scan. If it is set, it will ignore the config file value for the scan type.
                        Possible options: "quick" and "deep"
  -o, --output OUTPUT   The name of the output CSV and txt files, e.g. results.csv, results.txt, or results
  -s, --sitemap         Scan all internal links via loading sitemap?
  -D, --delay DELAY     Add a delay between scanning domains in seconds.
  -F, --output_format OUTPUT_FORMAT
                        The format (extension) of the output file Possible options: "csv", "json", "yaml", "txt", or
                        "all"
  -v, --verbose         Set the verbosity; a number between 1 and 5.
  --version             Get the version of the app.
```

### Examples
```bash
# Quick scan of one domain
domainia scan -d example.com -o out

# Deep scan, include sitemap pages, JSON + TXT outputs
domainia scan -d example.com -s -t deep -F json,txt -o out

# From a file, no delay, beautiful JSON
domainia scan -i domains.txt -D 0 -F json_beautiful -o out

# Multiple domains inline
domainia scan -d example.com,example.org -F all -o out
```

Tip: many defaults are configurable in `config.py` (scan switches, timeouts, output formats, etc.).
![Run Domainia Scanner](https://raw.githubusercontent.com/namnamir/domainia/main/img/scan.gif)

## 5. Results (CSV)
Result of the scan would be saved in a CSV file. You can manage the path of the output file by the argument `-o` or `--output`.
![Results in CSV](https://raw.githubusercontent.com/namnamir/domainia/main/img/result.png)
![Results in CSV](https://raw.githubusercontent.com/namnamir/domainia/main/img/result2.png)

## 6. JSON Format

```json
[
  "example.com": {
    "DNS": [
      {
        "record": "A",
        "value": "1.2.3.4",
      },
    ],
    "related_ip" : [
      {
        "name": "1.2.3.4",
        "version": "IPv4",
        "whois": {},
        "listed": [],
        "technologies" : [],
        "ports": [],
        "reverse_dns": [],
        "vulnerabilities": [],
      },
    ],
    "related_domains" : [
      {
        "name": "site.tld",
        "whois": {},
        "listed": [],
        "technologies" : [],
        "ports": [],
        "vulnerabilities": [],
        "http_headers": [],
        "html_meta": [],
        "subdomains": [],
        "related_domains": []
      },
    ],
    "html": {
      "meta": [
        {
          "name": "",
          "value": "",
        }
      ],
      "redirects": [],
      "status_code": 200,
      "title": "",
      "analytics": [
        {
          "name": "Google",
          "value": "UA-123"
        }
      ]
    },
    "http_headers": [
      {
        "name": "",
        "value": "",
      }
    ],
    "whois": {},
    "listed": [],
  }
]
```

---
⚖️ **Copyright**
Domainia tool is released under copy left; there is no right. Just kidding, it is under MIT license; read more about it on the [LICENSE page](https://github.com/namnamir/domainia/blob/main/LICENSE).

⚠️ **Disclaimer**
Domainia tool is tool for legitimate purposes. Do not use it in any illegitimate or illegal activities.
