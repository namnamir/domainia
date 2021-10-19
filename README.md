# Intro
**Domainia** is a tool find subdomains, DNS records, IP addresses, etc. of domain by using the passive and active reconnaissance techniques.

# How to Use

## 0- Install Dependencies
By running the following command, it will install all required dependencies.
```Bash
pip install requirements.txt
```

## 1- Add API Keys
Modify the file `api_keys.py` and add the API keys of the mentioned tools.

## 2- Check the Configuration File
Open the file `config.py` and modify it if needed. For each section of it, there is an explanation as the comment.

Specifically, define the `flags` because it has impacts on the speed of the whole process.

## 3- Run the Script
The script can be run in 2 modes, loading the list of domains from a file or from the command.
