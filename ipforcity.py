from zipfile import ZipFile

__author__ = 'stephenhenderson'

from collections import namedtuple

class CityToIpMap(namedtuple('CityToIpMap', 'city_to_ip')):

    def get_ip_for_city(self, city, country_code):
        city_key = make_city_key(city_name=city, country_code=country_code)
        return self.city_to_ip.get(city_key, None)

def make_city_key(city_name, country_code):
    return "{}:{}".format(country_code, city_name).lower()


def build_city_to_ip_map(city_file, ip_file):
    """
    Parses the maxmind geo-ip datasets and generates a dict of city-key (see
    make_city_key()) to ipv4 address.

    :param city_file: maxmind geo-ip city-locations csv
    :param ip_file: maxmind geo-ip city-blocks csv
    :return: dict of city-key to ipaddress
    """

    city_to_ip_address = dict()
    city_to_ip_range = build_city_to_ip_range_id_map(city_file)

    # See schema for ip-file here:
    # http://dev.maxmind.com/geoip/geoip2/geoip2-csv-databases/#Blocks_File
    ip_v4_prefix = "::ffff:"
    ip_v4_prefix_len = len(ip_v4_prefix)

    print("Reading ip-ranges from {} ...".format(ip_file.name))
    for line in ip_file:
        if line.startswith(ip_v4_prefix):
            fields = line.split(",")
            ip_address = fields[0][ip_v4_prefix_len:]
            ip_range_id = fields[2]
            city_key = city_to_ip_range.get(ip_range_id, None)
            if not city_key is None:
                city_to_ip_address[city_key] = ip_address
    print("Built map of {} city to ip-address entries".format(str(len(city_to_ip_address))))
    return city_to_ip_address


def build_city_to_ip_range_id_map(city_file):
    print("Extracting ip-ranges for cities from {}".format(city_file.name))
    city_to_ip_range = dict()
    first_line = True

    # See schema for city locations file here:
    # http://dev.maxmind.com/geoip/geoip2/geoip2-csv-databases/#Location_File
    for line in city_file:
        if first_line:
            # Skip csv header
            first_line = False
            continue
        fields = line.split(",")
        ip_range_id = fields[0]
        country_code = fields[3]
        city_name = fields[7].strip('"')
        city_key = make_city_key(city_name=city_name, country_code=country_code)
        city_to_ip_range[ip_range_id] = city_key

    print("Found {} ip-ranges".format(str(len(city_to_ip_range))))
    return city_to_ip_range
