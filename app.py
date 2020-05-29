from flask import Flask, render_template
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
epic_nick = 'HomeBredPine999'

def getPlayerStats(platform, epicNick):
    # GET https://api.fortnitetracker.com/v1/profile/{platform}/{epic-nickname} 
    endpoint = "https://api.fortnitetracker.com/v1/profile" + "/" + platform + "/" + epicNick
    #res = requests.request("GET", endpoint, headers=headers)
    res = requests.get( endpoint, headers = headers )
    return res.json

@app.route('/', methods=['GET'])
def home():
    data = getPlayerStats(plat, epic_nick)
    print(data.get('lifeTimeStats', 'Not Found!'))
    return render_template('test.html', data=data, epic_nick=epic_nick, platform=plat)


# @app.route('/match-history', methods=['GET'])
# def match():
#     response=requests.request("GET", url, headers=headers)
#     print(response.status_code)
#     return render_template(response)

if __name__ == '__main__':
    app.run(debug=True)
    pass