#!/usr/bin/env python

from typing import Dict
from bs4 import BeautifulSoup
import re


def hashable_finder(soup: BeautifulSoup, directive: str) -> Dict:
    """
    This function generates hash (SHA-256, SHA-384, or SHA-512 -> Base64) that is used by
    CSP directives 'child-src', 'connect-src', 'default-src', 'font-src', 'frame-src', 'img-src',
    'manifest-src', 'media-src', 'object-src', 'prefetch-src', 'script-src', 'script-src-elem',
    'script-src-attr', 'style-src', 'style-src-elem', 'style-src-attr', 'worker-src'.

    The hashing mechanism works like below:
    echo -n <TERM> | openssl sha256 -binary | openssl base64

    for more information read more on below links:
    - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/Sources
    - https://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy
    - https://w3c.github.io/webappsec-csp

    Args:
        soup (BeautifulSoup): the BeautifulSoup format of the HTML page
        directive (src): the name of the directive

    Returns:
        hashables (dict): a dictionary contains all unique contents that can be hashed
    """
    # a variable to store list of hashable elements, attributes, and events
    hashables = {
        'base-uri': set(),
        'child-src': set(),
        'connect-src': set(),
        'default-src': set(),
        'font-src': set(),
        'frame-src': set(),
        'img-src': set(),
        'manifest-src': set(),
        'media-src': set(),
        'object-src': set(),
        'prefetch-src': set(),
        'script-src': set(),
        'script-src-elem': set(),
        'script-src-attr': set(),
        'style-src': set(),
        'style-src-elem': set(),
        'style-src-attr': set(),
        'worker-src': set(),
    }
    # some variables to store styles and scripts in BS4 tag and text formats
    styles = []    # BS4 tag format
    styles_ = []   # text format
    scripts = []   # BS4 tag format
    scripts_ = []  # text format

    # list of JavaScript events that can be used in any HTML element
    # i.e., <button onclick='{JavaScript}'>
    javascript_events = [
        "onafterprint",
        "onafterscriptexecute",
        "onanimationcancel",
        "onanimationend",
        "onanimationiteration",
        "onanimationstart",
        "onauxclick",
        "onbeforecopy",
        "onbeforecut",
        "onbeforeprint",
        "onbeforescriptexecute",
        "onbeforeunload",
        "onbegin",
        "onblur",
        "onbounce",
        "oncanplay",
        "oncanplaythrough",
        "onchange",
        "onclick",
        "onclose",
        "oncontextmenu",
        "oncopy",
        "oncuechange",
        "oncut",
        "ondblclick",
        "ondrag",
        "ondragend",
        "ondragenter",
        "ondragleave",
        "ondragover",
        "ondragstart",
        "ondrop",
        "ondurationchange",
        "onend",
        "onended",
        "onerror",
        "onfocusin",
        "onfocusout",
        "onfullscreenchange",
        "onhashchange",
        "oninput",
        "oninvalid",
        "onkeydown",
        "onkeypress",
        "onkeyup",
        "onload",
        "onloadeddata",
        "onloadedmetadata",
        "onloadend",
        "onloadstart",
        "onmessage",
        "onmousedown",
        "onmouseenter",
        "onmouseleave",
        "onmousemove",
        "onmouseout",
        "onmouseover",
        "onmouseup",
        "onmousewheel",
        "onmozfullscreenchange",
        "onpagehide",
        "onpageshow",
        "onpaste",
        "onpause",
        "onplay",
        "onplaying",
        "onpointerdown",
        "onpointerenter",
        "onpointerleave",
        "onpointermove",
        "onpointerout",
        "onpointerover",
        "onpointerrawupdate",
        "onpointerup",
        "onpopstate",
        "onprogress",
        "onrepeat",
        "onreset",
        "onresize",
        "onscroll",
        "onsearch",
        "onseeked",
        "onseeking",
        "onselect",
        "onselectionchange",
        "onselectstart",
        "onshow",
        "onstart",
        "onsubmit",
        "ontoggle",
        "ontouchend",
        "ontouchmove",
        "ontouchstart",
        "ontransitioncancel",
        "ontransitionend",
        "ontransitionrun",
        "ontransitionstart",
        "onunhandledrejection",
        "onunload",
        "onvolumechange",
        "onwebkitanimationend",
        "onwebkitanimationiteration",
        "onwebkitanimationstart",
        "onwebkittransitionend",
        "onwheel",
    ]

    # get the content of attributes of <base href='{URL}'> elements
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/base-uri
    if directive == 'base-uri':
        hashables[directive].update(set(el['href'] for el in soup.findAll('base', href=True, nonce=False)))

    # get data related to <ifram> and related JavaScript APIs
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/child-src
    if directive in ['default-src', 'child-src']:
        # get the content of attributes of <iframe src='{URL}'> elements
        hashables[directive].update(set(el['src'] for el in soup.findAll('iframe', src=True, nonce=False)))
        # get <script> element contents
        scripts = soup.findAll('script', src=False, nonce=False) if not scripts else []
        # convert <script> element contents to string
        scripts_ = ' '.join([str(script) for script in scripts]) if not scripts_ else []
        # look for links in selected JavaScript APIs and add them to the set
        # the 're.DOTALL' flag is used to make the . character match newlines as well
        regex = r'Worker\s*\(["|\'](.*?)["|\']\)'
        hashables[directive].update(set(re.findall(regex, scripts_, re.DOTALL | re.IGNORECASE)))

    # get the content of attributes of <a ping='{URL}'> elements
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/connect-src
    if directive in ['default-src', 'connect-src']:
        hashables[directive].update(set(el['ping'] for el in soup.findAll('a', ping=True, nonce=False)))

    # get the content of attributes of <style>@font-face {src: url('{URL}'); }</script> elements
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/font-src
    if directive in ['default-src', 'font-src']:
        # get <style> element contents
        styles = soup.findAll('style', nonce=False) if not styles else []
        # convert <style> element contents to string
        styles_ = ' '.join([str(style) for style in styles]) if not styles_ else []
        # look for 'url's in '@import' rule and add them to the set
        # the 're.DOTALL' flag is used to make the . character match newlines as well
        regex = r'@font-face\s*.*?src\s*:\s*url\s*\(["|\'](.*?)["|\']\)'
        hashables[directive].update(set(re.findall(regex, styles_, re.DOTALL | re.IGNORECASE)))

    # get the content of attributes of <form action='{JavaSctript}'> elements
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/form-action
    if directive in ['default-src', 'form-action']:
        hashables[directive].update(set(el['action'] for el in soup.findAll('form', action=True, nonce=False)))

    # get the content of attributes of <iframe src='{URL}'> elements
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/frame-src
    if directive in ['default-src', 'frame-src']:
        hashables[directive].update(set(el['src'] for el in soup.findAll('iframe', src=True, nonce=False)))

    # get the content of attributes of <img src='{URL}'> elements
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/img-src
    if directive in ['default-src', 'img-src']:
        hashables[directive].update(set(el['src'] for el in soup.findAll('img', src=True, nonce=False)))

    # get the content of attributes of <link rel='manifest' href='{URL}'> elements
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/manifest-src
    if directive in ['default-src', 'manifest-src']:
        hashables[directive].update(set(el['href'] for el in soup.findAll('link', href=True,
                                                                          rel='manifest', nonce=False)))

    # get the content of attributes of <audio src='{URL}'> elements
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/media-src
    if directive in ['default-src', 'media-src']:
        hashables[directive].update(set(el['src'] for el in soup.findAll(['audio', 'video', 'track'],
                                                                         src=True, nonce=False)))

    # get the content of attributes of <embed src='{URL}'>, <object data='{URL}'>, or <applet archive='{URL}'> elements
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/object-src
    if directive in ['default-src', 'media-src']:
        hashables[directive].update(set(el['src'] for el in soup.findAll('embed', src=True, nonce=False)))
        hashables[directive].update(set(el['data'] for el in soup.findAll('object', data=True, nonce=False)))
        hashables[directive].update(set(el['archive'] for el in soup.findAll('applet', archive=True, nonce=False)))

    # get the content of all <script>{JavaScript}<script> elements and events
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/script-src
    if directive in ['default-src', 'script-src']:
        # get <script> element contents and add them to the set
        scripts = soup.findAll('script', src=False, nonce=False) if not scripts else []
        hashables[directive].update(set(el.text for el in scripts))

    # iterate over JavaScript events
    # events like <button onclick="send_form();">Send</button>
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/script-src-attr
    if directive in ['default-src', 'script-src-attr']:
        # find any HTML element contains the event: hashable in soup.select(f'[{event}]')
        hashables[directive].update(set(el[event] for event in javascript_events
                                        for el in soup.select(f'[{event}]')))

    # get the content of attributes of <script src='{url}'> elements
    # read more: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src-elem
    if directive in ['default-src', 'script-src-elem']:
        hashables[directive].update(set(el['src'] for el in soup.findAll('script', src=True, nonce=False)))

    # add the content of all <style>{CSS}</style> elements
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/style-src
    if directive in ['default-src', 'style-src']:
        # get <style> element contents
        styles = soup.findAll('style', nonce=False) if not styles else []
        hashables[directive].update(set(el.text for el in styles))

    # add the content of attributes of <p style='{CSS}'> elements
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/style-src-attr
    if directive in ['default-src', 'style-src-attr']:
        hashables[directive].update(set(el['style'] for el in soup.select('[style]')))

    # add the content of attributes of <link rel='stylesheet' href='{url}'> elements
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/style-src-elem
    if directive in ['default-src', 'style-src-elem']:
        # add the content of attributes of <link rel='stylesheet' href='{url}'> elements
        hashables[directive].update(set(el['href'] for el in soup.findAll('link', href=True,
                                                                          rel='stylesheet', nonce=False)))
        # get <style> element contents
        styles = soup.findAll('style', nonce=False) if not styles else []
        # convert <style> element contents to string
        styles_ = ' '.join([str(style) for style in styles]) if not styles_ else []
        # look for 'url's in '@import' rule and add them to the set
        # the 're.DOTALL' flag is used to make the . character match newlines as well
        regex = r'@import\s+url\s*\(["|\'](.*?)["|\']\)'
        hashables[directive].update(set(re.findall(regex, styles_, re.DOTALL | re.IGNORECASE)))

    # get the content of attributes of <script>Worker('{URL}')</script>, <script>SharedWorker('{URL}')</script>, and
    # <script>serviceWorker.register('{URL}')</script> elements
    # read more: http://udn.realityripple.com/docs/Web/HTTP/Headers/Content-Security-Policy/worker-src
    if directive in ['default-src', 'worker-src']:
        # get <script> element contents
        scripts = soup.findAll('script', src=False, nonce=False) if not scripts else []
        # convert <script> element contents to string
        scripts_ = ' '.join([str(script) for script in scripts]) if not scripts_ else []
        # look for links in selected JavaScript APIs and add them to the set
        # the 're.DOTALL' flag is used to make the . character match newlines as well
        regex = r'[Worker|SharedWorker|serviceWorker\.register]\s*\(["|\'](.*?)["|\']\)'
        hashables[directive].update(set(re.findall(regex, scripts_, re.DOTALL | re.IGNORECASE)))

    # return results
    return hashables
