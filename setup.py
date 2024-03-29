#!/usr/bin/env python

from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent

with open(this_directory / 'README.md', 'r', encoding='utf-8') as readme_file:
    README = readme_file.read()

with open(this_directory / 'CHANGELOG.md', 'r', encoding='utf-8') as changelog_file:
    CHANGELOG = changelog_file.read()

setup_args = dict(
    name='Domainia',
    version='2.0.1',
    description='Domainia helps to find subdomains, DNS records, IP addresses, SSL Certificates, HTTP info, etc. of domain by doing the passive reconnaissance.',
    long_description=README + '\n\n' + CHANGELOG,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    author='Ali N. / IRSec',
    author_email='hi@irsec.eu',
    keywords=[
        'dns', 'ssl', 'osint', 'certificate', 'ipv6', 'whois', 'ipv4', 
        'subdomain', 'ip', 'ssl-certificates', 'whois-lookup', 'certifi', 
        'subdomain-scanner', 'subdomain-enumeration', 'osint-python', 'scanner'
    ],
    url='https://github.com/namnamir/domainia',
    download_url='https://pypi.org/project/domainia/',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

install_requires = [
    'beautifulsoup4==4.11.1',
    'colorama==0.4.5',
    'cryptography==38.0.1',
    'dnspython==2.2.1',
    'requests==2.28.1',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
