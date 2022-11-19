from .base import UdgerBase

from .queries import Queries


class UaRequest(object):
    def __init__(self, ua_string=None, sec_ch_ua=None, sec_ch_ua_full_version_list=None, sec_ch_ua_mobile=None,
                 sec_ch_ua_full_version=None, sec_ch_ua_platform=None, sec_ch_ua_platform_version=None, sec_ch_ua_model=None):
        self.ua_string = ua_string
        self.sec_ch_ua = sec_ch_ua
        self.sec_ch_ua_full_version_list = sec_ch_ua_full_version_list.strip('"') if sec_ch_ua_full_version_list else None
        self.sec_ch_ua_mobile = sec_ch_ua_mobile
        self.sec_ch_ua_full_version = sec_ch_ua_full_version.strip('"') if sec_ch_ua_full_version else None
        self.sec_ch_ua_platform = sec_ch_ua_platform.strip('"') if sec_ch_ua_platform else None
        self.sec_ch_ua_platform_version = sec_ch_ua_platform_version.strip('"') if sec_ch_ua_platform_version else None
        self.sec_ch_ua_model = sec_ch_ua_model.strip('"') if sec_ch_ua_model else None

    def cache_key(self):
        return '[uaString=' + (self.ua_string if self.ua_string is not None else '') + \
                ', secChUa=' + (self.sec_ch_ua if self.sec_ch_ua is not None else '') + \
                ', secChUaFullVersionList=' + (self.sec_ch_ua_full_version_list if self.sec_ch_ua_full_version_list is not None else '') + \
                ', secChUaMobile=' + (self.sec_ch_ua_mobile if self.sec_ch_ua_mobile is not None else '') + \
                ', secChUaFullVersion=' + (self.sec_ch_ua_full_version if self.sec_ch_ua_full_version is not None else '') + \
                ', secChUaPlatform=' + (self.sec_ch_ua_platform if self.sec_ch_ua_platform is not None else '') + \
                ', secChUaPlatformVersion=' + (self.sec_ch_ua_platform_version if self.sec_ch_ua_platform_version is not None else '') + \
                ', secChUaModel=' + (self.sec_ch_ua_model if self.sec_ch_ua_model is not None else '') + ']'


class Udger(UdgerBase):

    def parse_ua(self, ua_string):
        ua_request = UaRequest(ua_string=ua_string)
        return self.parse_ua_request(ua_request)

    def parse_ua_request(self, ua_request):

        cache_key = None
        if self.lru_cache is not None and ua_request is not None:
            cache_key = ua_request.cache_key()
            cached = self.lru_cache.get(cache_key, None)
            if cached is not None:
                return cached

        ua, class_id, client_id = self._process_client(ua_request.ua_string)
        is_crawler = (ua['ua_class'] == 'Crawler')

        opsys = self._process_os(ua_request.ua_string, client_id) if not is_crawler else None
        ua.update(opsys or self.os_emptyrow)

        dev = self._process_device(ua_request.ua_string, class_id) if not is_crawler else None
        ua.update(dev or self.device_emptyrow)

        marketname = self._process_marketname(ua, ua_request.ua_string, class_id) if not is_crawler and ua['os_family_code'] else None
        ua.update(marketname or self.marketname_emptyrow)

        if ua.get('ua_class_code') != 'Crawler' and self.client_hints_parser_enabled:
            ua.update(vars(ua_request))
            self._process_client_hints(ua, ua_request)
        else:
            ua['ua_string'] = ua_request.ua_string

        if cache_key is not None:
            self.lru_cache[cache_key] = ua

        return ua

    def parse_ip(self, ip_string):
        ip = self.ip_datacenter_emptyrow.copy()
        ip['ip'] = ip_string

        try:
            ip_string, ipv4_int, ipv6_words = self.normalize_ipaddress(ip_string)
        except:
            pass
        else:
            ip.update(
                ip_classification='Unrecognized',
                ip_classification_code='unrecognized',
            )

            ip_row = self.db_get_first_row(Queries.ip_sql, ip_string)
            if ip_row:
                if ip_row['ip_classification_code'] != 'crawler':
                    ip_row.pop('crawler_family_info_url')

                ip.update(ip_row)

            if ipv4_int is not None:
                ip['ip_ver'] = 4
                dc = self.db_get_first_row(Queries.datacenter_sql, ipv4_int, ipv4_int)

            else:
                ip['ip_ver'] = 6
                ipv6_words *= 2
                dc = self.db_get_first_row(Queries.datacenter6_sql, *ipv6_words)

            if dc:
                ip.update(dc)

        return ip

    def _process_client(self, ua_string):
        ua = self.db_get_first_row(Queries.crawler_sql, ua_string)
        if ua:
            del ua['class_id']
            del ua['client_id']
            class_id = 99
            client_id = -1
        else:
            rowid = self._find_id_from_list(ua_string, self.client_word_detector.find_words(ua_string), self.client_regstring_list)
            if rowid != -1:
                ua = self.db_get_first_row(Queries.client_sql, rowid)
                self._patch_versions(ua)
            else:
                ua = self.client_emptyrow.copy()
            class_id = ua.pop('class_id', -1)
            client_id = ua.pop('client_id', 0)
        return ua, class_id, client_id

    def _process_os(self, ua_string, client_id):
        rowid = self._find_id_from_list(ua_string, self.os_word_detector.find_words(ua_string), self.os_regstring_list)
        if rowid != -1:
            return self.db_get_first_row(Queries.os_sql, rowid)
        return client_id != 0 and self.db_get_first_row(Queries.client_os_sql, client_id)

    def _process_device(self, ua_string, class_id):
        rowid = self._find_id_from_list(ua_string, self.device_word_detector.find_words(ua_string), self.device_regstring_list)
        if rowid != -1:
            return self.db_get_first_row(Queries.device_sql, rowid)
        return class_id != -1 and self.db_get_first_row(Queries.client_class_sql, class_id)

    def _process_marketname(self, ua, ua_string, class_id):
        marketname = None
        # must complete first so cursors don't collide
        rows = tuple(self.db_iter_rows(
            Queries.devicename_sql,
            ua['os_family_code'],
            ua['os_code'],
        ))

        for dn_row in rows:
            if self.regexp_func(dn_row['regstring'], ua_string):
                match = self.last_regexp_match.group(1)

                marketname = self.db_get_first_row(
                    Queries.marketname_sql,
                    dn_row['regex_id'],
                    match.strip(),
                )
                if marketname:
                    break
        return marketname

    def _process_client_hints(self, ua, ua_request):

        if not ua_request.sec_ch_ua_mobile:
            sec_ch_ua_mobile = 0
            ua['sec_ch_ua_mobile'] = ''
        else:
            if ua_request.sec_ch_ua_mobile == '?0':
                sec_ch_ua_mobile = 0
            else:
                sec_ch_ua_mobile = 1
            ua['sec_ch_ua_mobile'] = sec_ch_ua_mobile

        regstring_search1 = ua_request.sec_ch_ua_full_version_list

        if not regstring_search1:
            regstring_search1 = ua_request.sec_ch_ua

        if regstring_search1:
            rows1 = tuple(self.db_iter_rows(Queries.client_ch_regex_sql, sec_ch_ua_mobile))

            for dn_row in rows1:
                regex = dn_row['regstring']
                if regex and self.regexp_func(regex, regstring_search1):
                    ver = self.last_regexp_match.group(1)

                    if ua_request.sec_ch_ua_full_version_list:
                        dot_index = ver.find('.')
                        ver_major = ver[0:dot_index] if dot_index >= 0 else ver
                    else:
                        ver_major = ver
                        if ua_request.sec_ch_ua_full_version:
                            ver = ua_request.sec_ch_ua_full_version

                    ua['ua_class'] = dn_row['client_classification']
                    ua['ua_class_code'] = dn_row['client_classification_code']
                    ua['ua'] = dn_row['name'] + ' ' + ver
                    ua['ua_version'] = ver
                    ua['ua_version_major'] = ver_major
                    ua['ua_uptodate_current_version'] = dn_row['uptodate_current_version']
                    ua['ua_family'] = dn_row['name']
                    ua['ua_family_code'] = dn_row['name_code']
                    ua['ua_family_homepage'] = dn_row['homepage']
                    ua['ua_family_vendor'] = dn_row['vendor']
                    ua['ua_family_vendor_code'] = dn_row['vendor_code']
                    ua['ua_family_vendor_homepage'] = dn_row['vendor_homepage']
                    ua['ua_family_icon'] = dn_row['icon']
                    ua['ua_family_icon_big'] = dn_row['icon_big']
                    ua['ua_family_info_url'] = dn_row['ua_family_info_url']
                    ua['ua_engine'] = dn_row['engine']
                    break

        regstring_search2 = ua_request.sec_ch_ua_platform
        if regstring_search2:
            rows2 = tuple(self.db_iter_rows(Queries.os_ch_regex_sql,
                                            ua_request.sec_ch_ua_platform_version if ua_request.sec_ch_ua_platform_version else ''))

            for dn_row in rows2:
                    regex = dn_row['regstring']
                    if regex and self.regexp_func(regex, regstring_search2):
                        ua['os'] = dn_row['name']
                        ua['os_code'] = dn_row['name_code']
                        ua['os_homepage'] = dn_row['homepage']
                        ua['os_icon'] = dn_row['icon']
                        ua['os_icon_big'] = dn_row['icon_big']
                        ua['os_info_url'] = dn_row['os_info_url']
                        ua['os_family'] = dn_row['family']
                        ua['os_family_code'] = dn_row['family_code']
                        ua['os_family_vendor'] = dn_row['vendor']
                        ua['os_family_vendor_code'] = dn_row['vendor_code']
                        ua['os_family_vendor_homepage'] = dn_row['vendor_homepage']
                        break

        if ua_request.sec_ch_ua_model and ua['os_family_code']:
            row3 = self.db_get_first_row(Queries.device_name_ch_regex_sql, ua['os_family_code'], ua['os_family_code'], ua['os_code'])
            if row3:
                row4 = self.db_get_first_row(Queries.device_name_list_ch_sql, row3['id'], ua_request.sec_ch_ua_model)
                if row4:
                    ua['device_marketname'] = row4['marketname']
                    ua['device_brand'] = row4['brand']
                    ua['device_brand_code'] = row4['brand_code']
                    ua['device_brand_homepage'] = row4['brand_url']
                    ua['device_brand_icon'] = row4['icon']
                    ua['device_brand_icon_big'] = row4['icon_big']
                    ua['device_brand_info_url'] = row4['brand_info_url']

                    row5 = self.db_get_first_row(Queries.device_class_ch_sql, row4['deviceclass_id'])
                    if row5:
                        ua['device_class'] = row5['device_class']
                        ua['device_class_code'] = row5['device_class_code']
                        ua['device_class_icon'] = row5['device_class_icon']
                        ua['device_class_icon_big'] = row5['device_class_icon_big']
                        ua['device_class_info_url'] = row5['device_class_info_url']


        if not ua['device_class'] and ua['ua_class_code']:
            row6 = self.db_get_first_row(Queries.device_class_by_mobile_ch_sql, sec_ch_ua_mobile)
            if row6:
                    ua['device_class'] = row6['device_class']
                    ua['device_class_code'] = row6['device_class_code']
                    ua['device_class_icon'] = row6['device_class_icon']
                    ua['device_class_icon_big'] = row6['device_class_icon_big']
                    ua['device_class_info_url'] = row6['device_class_info_url']

    def _find_id_from_list(self, ua_string, found_client_words, reg_string_list):
        self.last_regexp_match = None
        for irs in reg_string_list:
            if (irs.word_id in found_client_words) and (irs.word2_id in found_client_words):
                m = irs.pattern.search(ua_string)
                if m is not None:
                    self.last_regexp_match = m
                    return irs.rowid
        return -1

    def _patch_versions(self, ua):
        if self.last_regexp_match:
            try:
                ver = self.last_regexp_match.group(1)
            except IndexError:
                ver = ''

            ua['ua_version'] = ver
            ua['ua'] += ' ' + ver
            ua['ua_version_major'] = ver.split('.')[0]
        else:
            ua['ua_version'] = ua['ua_version_major'] = None

