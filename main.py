__author__ = 'stephenhenderson'

import os, gzip
from ipforcity import *
from flask import Flask, request, render_template

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def ip_for_city_lookup():
    city_name = request.args.get("city_name", None)
    country_code = request.args.get("country_code", None)
    if city_name is None or country_code is None:
        return render_template('layout.html')
    else:
        ip_address = city_to_ip_map.get_ip_for_city(city_name, country_code)
        return render_template('ip_lookup.html',
                               ip_address=ip_address,
                               city_name=city_name,
                               country_code=country_code)

def populate_city_to_ip_map():
    print("Populating city to ip map...")
    with gzip.open("GeoLite2-City-Locations.csv.gz") as city_file:
        with gzip.open("GeoLite2-City-Blocks.csv.gz") as ip_range_file:
            return build_city_to_ip_map(city_file, ip_range_file)

city_to_ip_map = CityToIpMap(city_to_ip=populate_city_to_ip_map())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, use_reloader=False)
