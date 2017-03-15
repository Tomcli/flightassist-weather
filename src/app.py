import os, json, requests
from flask import Flask, Response, abort, request
from datetime import datetime
import logging
from logging import StreamHandler
#import urllib3

#urllib3.disable_warnings()
# Define the base logger
logging.getLogger("weather-service").setLevel(logging.DEBUG)
log = logging.getLogger("weather-service")
stream_handler = StreamHandler()
stream_formatter = logging.Formatter('[%(asctime)s] [%(thread)d] [%(module)s : %(lineno)d] [%(levelname)s] %(message)s')
stream_handler.setFormatter(stream_formatter)
log.addHandler(stream_handler)

# Flask config
app = Flask(__name__, static_url_path='')
app.config['PROPAGATE_EXCEPTIONS'] = True

# other global variables
WEATHER_EP = os.environ['WEATHER_URL']

'''
 This is the analyzer API that accepts GET data as describes below:
 GET http://localhost:5000/weather
'''
@app.route('/weather/<lat>/<lon>', methods=['GET'])
def get_weather(lat, lon):

    weather_service_ep = WEATHER_EP + '/api/weather/v1/geocode/' + lat + '/' + lon + '/forecast/daily/3day.json'
    log.info(weather_service_ep)
    r = requests.get(weather_service_ep, headers={'Content-type': 'application/json'})
    if r.status_code != 200:
        log.error("FAILED retrieve weather information: '%s', msg: '%s'", input_text, r.text)
        return None
    #return r
    log.info(r.text)
    response = Response(json.dumps(r.text))
    response.headers['Content-Type'] = 'application/json'
    response.status_code = r.status_code

    return response


if __name__ == '__main__':
    # construct weateher_ep from env var or vcap_services
    PORT = os.getenv('VCAP_APP_PORT', '5000')

    log.info("Starting weather service weather_service:")
    app.run(host='0.0.0.0', port=int(PORT))
