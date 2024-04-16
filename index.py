#!/usr/bin/python3

import logging
from flask import Flask, request, send_file
import requests
import json
import subprocess


app = Flask(__name__)

@app.route('/anadrop')
def download_file():
    return send_file('dns_entries.txt', as_attachment=True)



logging.basicConfig(filename='anareceive.log', level=logging.INFO)

# @app.route('/oficio', methods=['GET'])
# def receive_url():
#     url = request.args.get('url')
#     logging.info(url)
#     return 'OK'



# @app.route('/oficio', methods=['GET'])
# def receive_url():
#     # url = request.args.get('url')
#     if url.startswith('/oficio='):
#         url = url[8:]
#     logging.info(url)

#     # Execute the import_from_url.py script with the received URL as an argument
#     subprocess.call(['/usr/bin/python3', '/anatel/import_from_url.py', url])

#     return 'OK'



# def import_from_url(url):
#     # Send a GET request to the URL to retrieve the data
#     response = requests.get(url)

#     # Parse the JSON response
#     data = json.loads(response.text)

#     # Process the data and import it into your database or other system

#     # Return a success message
#     return 'OK'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1984)
