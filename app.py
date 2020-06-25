from flask import Flask, request, render_template
import requests
import configparser

# Running this requires an API key and a file 
# containing the API key as follows: settings.ini
def get_config_data():
    config = configparser.ConfigParser()
    config.read ('settings.ini')
    return config

# get API key from file--keep separated for security
api_config = get_config_data()
key_name = 'TRN-API-Key'
key_data = api_config['API-Key'][key_name]
headers={ key_name: key_data }
app = Flask(__name__)

# default route
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
    # return the collected data 
    return r.json()

@app.route('/stats/', methods=['GET', 'POST'])
def lifeTimeStats():
    if request.method == 'POST':
        try:
            name = request.form['user-name']
        except:
            return(404)
        try:
            plat = request.form['plat']
        except:
            return(404)

    # collected fields from user, now go get the stats!
    stats = getPlayerStats(plat, name)

    # check for player not found, returned as a dict
    # {'error' : 'Player Not Found'}
    err = stats.get('error') 
    if err:
        print(stats['error'])
        if stats['error'] == 'Player Not Found':
            return render_template('error.html', player=name, platform=plat )

    # normal flow. present the stats page        
    return render_template('stats.html', epic_nick=name, platform=plat, data=stats)

# For page request that is not found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

# Future ideas: have selectedable player stats: Solos
# Duos, Squads, Lifetime
# Have the shop details presented
# More?

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    pass