from flask import Flask, request, render_template
import requests
import configparser
import json

def get_config_data():
    # later add parameter for file path, and possibly, sections
    config = configparser.ConfigParser()
    config.read ('settings.ini')
    return config

# get API key from file--keep separated for security
api_config = get_config_data()
key_name = 'TRN-API-Key'
key_data = api_config['API-Key'][key_name]
headers={ key_name: key_data }
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

def getLifetimeStats(data):
    lifeTimeStats = {}
    for d in data['lifeTimeStats']:
        lifeTimeStats[d['key']] = d['value']
    return lifeTimeStats

def getPlayerStats(platform, epicNick):
    # GET https://api.fortnitetracker.com/v2/profile/{platform}/{epic-nickname} 
    endpoint = "https://api.fortnitetracker.com/v1/profile" + "/" + platform + "/" + epicNick

    # make a request and handle most common HTTP errors
    try:
        r = requests.get( endpoint, headers = headers )
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

    return r.json()

@app.route('/stats/', methods=['GET', 'POST'])
def lifeTimeStats():
    # need a check to see that playername exists on the Fortnite stats server
    # and conditionally display the correct response: found (and stats)
    if request.method == 'POST':
        try:
            name = request.form['user-name']
        except:
            return(404)
        try:
            plat = request.form['plat']
        except:
            return(404)

    stats = getPlayerStats(plat, name)

    err = stats.get('error') 
    if err:
        print(stats['error'])
        if stats['error'] == 'Player Not Found':
            return render_template('error.html', player=name, platform=plat )

    # normal flow. present the stats page        
    return render_template('stats.html', epic_nick=name, platform=plat, data=stats)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

# @app.route('/match-history', methods=['GET'])
# def match():
#     response=requests.request("GET", url, headers=headers)
#     print(response.status_code)
#     return render_template(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    pass