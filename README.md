# Udger client for Python (data ver. 4)

Local parser is very fast and accurate useragent string detection solution. Enables developers to locally install and integrate a highly-scalable product.
We provide the detection of the devices (personal computer, tablet, Smart TV, Game console etc.), operating system and client SW type (browser, e-mail client etc.).
It also provides information about IP addresses (Public proxies, VPN services, Tor exit nodes, Fake crawlers, Web scrapers .. etc.)

- Tested with more the 50.000 unique user agents.
- Up to date data provided by https://udger.com/
- Support for Python 3

Enjoy!

### Install using pip

    $ pip install udger-v4

### Install from git repo

    $ git clone https://github.com/udger/udger-python-v4
    $ cd udger-python-v4/
    # python setup.py install

### Automatic updates download

For data auto update, please use Udger data updater (https://udger.com/support/documentation/?doc=62)

### Help us

Feel free to send us a Pull Request on GitHub to help us make Udger for Python better.
Or just let us know of any issues you encounter.

Thank you!

### Usage

```
    $ python
    >>> from pprint import pprint
    >>> from udger import Udger
    >>> from udger import UaRequest
    >>> udger = Udger()
    >>>
    >>> result = udger.parse_ua(
    ...     'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'
    ... )
    >>> pprint(result)
    {'crawler_category': None,
     'crawler_category_code': None,
     'crawler_last_seen': None,
     'crawler_respect_robotstxt': None,
     'device_brand': 'Apple',
     'device_brand_code': 'apple',
     'device_brand_homepage': 'https://www.apple.com/',
     'device_brand_icon': 'apple.png',
     'device_brand_icon_big': 'apple_big.png',
     'device_brand_info_url': 'https://udger.com/resources/ua-list/devices-brand-detail?brand=apple',
     'device_class': 'Tablet',
     'device_class_code': 'tablet',
     'device_class_icon': 'tablet.png',
     'device_class_icon_big': 'tablet_big.png',
     'device_class_info_url': 'https://udger.com/resources/ua-list/device-detail?device=Tablet',
     'device_marketname': 'iPad',
     'os': 'iOS 7',
     'os_code': 'ios_7',
     'os_family': 'iOS',
     'os_family_code': 'ios',
     'os_family_vendor': 'Apple Inc.',
     'os_family_vendor_code': 'apple_inc',
     'os_family_vendor_homepage': 'https://www.apple.com/',
     'os_homepage': 'https://en.wikipedia.org/wiki/IOS_7',
     'os_icon': 'iphone.png',
     'os_icon_big': 'iphone_big.png',
     'os_info_url': 'https://udger.com/resources/ua-list/os-detail?os=iOS%207',
     'sec_ch_ua': None,
     'sec_ch_ua_full_version': None,
     'sec_ch_ua_full_version_list': None,
     'sec_ch_ua_mobile': '',
     'sec_ch_ua_model': None,
     'sec_ch_ua_platform': None,
     'sec_ch_ua_platform_version': None,
     'ua': 'Safari mobile 7.0',
     'ua_class': 'Mobile browser',
     'ua_class_code': 'mobile_browser',
     'ua_engine': 'WebKit',
     'ua_family': 'Safari mobile',
     'ua_family_code': 'safari_mobile',
     'ua_family_homepage': 'https://en.wikipedia.org/wiki/Safari_(web_browser)',
     'ua_family_icon': 'safari.png',
     'ua_family_icon_big': 'safari_big.png',
     'ua_family_info_url': 'https://udger.com/resources/ua-list/browser-detail?browser=Safari%20mobile',
     'ua_family_vendor': 'Apple Inc.',
     'ua_family_vendor_code': 'apple_inc',
     'ua_family_vendor_homepage': 'https://www.apple.com/',
     'ua_string': 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) '
                  'AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 '
                  'Mobile/11A465 Safari/9537.53',
     'ua_uptodate_current_version': '15',
     'ua_version': '7.0',
     'ua_version_major': '7'}
    >>>
    >>> ua_request=UaRequest(ua_string='',sec_ch_ua='" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"', 
    ...                      sec_ch_ua_full_version_list='', sec_ch_ua_mobile='?0', sec_ch_ua_full_version='"97.0.4692.71"', 
    ...                      sec_ch_ua_platform='', sec_ch_ua_platform_version='', sec_ch_ua_model=''
    >>> )
    >>>     
    >>> pprint(result)
    {'crawler_category': None,
     'crawler_category_code': None,
     'crawler_last_seen': None,
     'crawler_respect_robotstxt': None,
     'device_brand': None,
     'device_brand_code': None,
     'device_brand_homepage': None,
     'device_brand_icon': None,
     'device_brand_icon_big': None,
     'device_brand_info_url': None,
     'device_class': 'Desktop',
     'device_class_code': 'desktop',
     'device_class_icon': 'desktop.png',
     'device_class_icon_big': 'desktop_big.png',
     'device_class_info_url': 'https://udger.com/resources/ua-list/device-detail?device=Desktop',
     'device_marketname': None,
     'os': None,
     'os_code': None,
     'os_family': None,
     'os_family_code': None,
     'os_family_vendor': None,
     'os_family_vendor_code': None,
     'os_family_vendor_homepage': None,
     'os_homepage': None,
     'os_icon': None,
     'os_icon_big': None,
     'os_info_url': None,
     'sec_ch_ua': '" Not;A Brand";v="99", "Google Chrome";v="97", '
                  '"Chromium";v="97"',
     'sec_ch_ua_full_version': '97.0.4692.71',
     'sec_ch_ua_full_version_list': None,
     'sec_ch_ua_mobile': 0,
     'sec_ch_ua_model': None,
     'sec_ch_ua_platform': None,
     'sec_ch_ua_platform_version': None,
     'ua': 'Chrome 97.0.4692.71',
     'ua_class': 'Browser',
     'ua_class_code': 'browser',
     'ua_engine': 'WebKit/Blink',
     'ua_family': 'Chrome',
     'ua_family_code': 'chrome',
     'ua_family_homepage': 'http://www.google.com/chrome/',
     'ua_family_icon': 'chrome.png',
     'ua_family_icon_big': 'chrome_big.png',
     'ua_family_info_url': 'https://udger.com/resources/ua-list/browser-detail?browser=Chrome',
     'ua_family_vendor': 'Google Inc.',
     'ua_family_vendor_code': 'google_inc',
     'ua_family_vendor_homepage': 'https://about.google/',
     'ua_string': '',
     'ua_uptodate_current_version': '107',
     'ua_version': '97.0.4692.71',
     'ua_version_major': '97'}
    >>>     
    >>> result = udger.parse_ip('108.61.199.93')
    >>> pprint(result)
    {'crawler_category': 'Site monitor',
     'crawler_category_code': 'site_monitor',
     'crawler_family': 'PINGOMETER',
     'crawler_family_code': 'pingometer',
     'crawler_family_homepage': '',
     'crawler_family_icon': 'bot_pingometer.png',
     'crawler_family_info_url': 'https://udger.com/resources/ua-list/bot-detail?bot=PINGOMETER',
     'crawler_family_vendor': 'Pingometer, LLC',
     'crawler_family_vendor_code': 'pingometer_llc',
     'crawler_family_vendor_homepage': 'http://pingometer.com/',
     'crawler_last_seen': '2016-09-17 12:15:38',
     'crawler_name': 'PINGOMETER',
     'crawler_respect_robotstxt': 'no',
     'crawler_ver': '',
     'crawler_ver_major': '',
     'datacenter_homepage': 'https://www.choopa.com/',
     'datacenter_name': 'Choopa, LLC.',
     'datacenter_name_code': 'choopa',
     'ip': '108.61.199.93',
     'ip_city': 'Amsterdam',
     'ip_classification': 'Crawler',
     'ip_classification_code': 'crawler',
     'ip_country': 'Netherlands',
     'ip_country_code': 'NL',
     'ip_hostname': '108.61.199.93.vultr.com',
     'ip_last_seen': '2016-09-17 12:00:31',
     'ip_ver': 4}
```

### Data directory

``Udger()`` parser expects the data file to be placed in the system temporary
directory as returned by the ``tempfile.gettempdir()``.

You may override the path using the argument like this:

	udger = Udger('/var/cache/udger/')

### Documentation for developers

https://udger.com/pub/documentation/parser/Python-v4/html/

### Author

The Udger.com Team (info@udger.com)

### v3 format
For the previous data format (v3), please use https://github.com/udger/udger-python
