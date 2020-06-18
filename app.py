from flask import Flask, request, render_template
import requests
import configparser

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

plat = 'psn'

def getLifetimeStats(data):
    lifeTimeStats = {}
    for d in data['lifeTimeStats']:
        lifeTimeStats[d['key']] = d['value']
    return lifeTimeStats

def getPlayerStats(platform, epicNick):
    # GET https://api.fortnitetracker.com/v1/profile/{platform}/{epic-nickname} 
    endpoint = "https://api.fortnitetracker.com/v1/profile" + "/" + platform + "/" + epicNick
    res = requests.get( endpoint, headers = headers )
    return res.json()

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('landing.html')

@app.route('/stats/', methods=['GET', 'POST'])
def lifeTimeStats():
    # need a check to see that playername exists on the Fortnite stats server
    # and conditionally display the correct response: found (and stats)
    if request.method == 'POST':
        try:
            name = request.form['user-name']
        except:
            return(404)

    print('name = ', name)
    stats = getPlayerStats(plat, name)
    if stats['error'] == 'Player Not Found':
        return('<h1>Player not found in Epic\'s database.</h1>')
    print(stats)
    return render_template('stats.html', epic_nick=name, platform=plat, data=stats)

# @app.route('/match-history', methods=['GET'])
# def match():
#     response=requests.request("GET", url, headers=headers)
#     print(response.status_code)
#     return render_template(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    pass