import requests
import json
import urllib3
import sys

from flask import Flask, render_template

app = Flask(__name__)

def isBearClaimed(bullTokenIdDec):
    
    # Convert dec bullTokenIdDec to hex i.e. 7777 (Dec) -> 1E61 (hex)
    data=hex(int(hex(bullTokenIdDec), 16) ^ int(hex(0x45083abc0000000000000000000000000000000000000000000000000000000000000000), 16))

    url = "http://node1.web3api.com/"

    payload = json.dumps({
      "jsonrpc": "2.0",
      "id": 17,
      "method": "eth_call",
      "params": [
        {
          "from": "0x0000000000000000000000000000000000000000",
          "data": data,
          "to": "0x45ec819d71fcc4a2ea58ff70e66d4216c403a424"
        },
        "latest"
      ]
    })
    headers = {
      'authority': 'node1.web3api.com',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',
      'content-type': 'application/json',
      'accept': '*/*',
      'sec-gpc': '1',
      'origin': 'https://etherscan.io',
      'sec-fetch-site': 'cross-site',
      'sec-fetch-mode': 'cors',
      'sec-fetch-dest': 'empty',
      'referer': 'https://etherscan.io/',
      'accept-language': 'en-US,en;q=0.9'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)
    claimed="Not claimed his bear"
    if(response_dict["result"] != "0x0000000000000000000000000000000000000000000000000000000000000000"):
        claimed = "Claimed his bear"
    resp={
        'openseaUrl': 'https://opensea.io/assets/0x469823c7b84264d1bafbcd6010e9cdf1cac305a3/' + str(bullTokenIdDec),
        'tokenURI': "https://www.cryptobullsociety.com/metadata/" + str(bullTokenIdDec) + ".json",
        'imgURL': 'https://cryptobullsociety.com/images/'+str(bullTokenIdDec)+'.png',
        'claimed': str(claimed)
        }
    return resp



@app.route('/')
def firstRoute():
        return '''
        <h1>Crypto Bull #{}</h1>
        <img src="{}" height="150" width="150" ></img>
        </br>
        </br>
        <a href="{}">Traits</a>
        <h3>{}</h3>
        <a href="{}">Buy on opensea!</h1>
        '''.format("-/-","","","Whoops.. try again","",)
        
# index
@app.route('/<int:tokenId>')
def index(tokenId):
    if tokenId <= 7777 and tokenId > 0: 
        data=isBearClaimed(tokenId)
        return '''
        <h1>Crypto Bull #{}</h1>
        <img src="{}" height="150" width="150" ></img>
        </br>
        </br>
        <a href="{}">Traits</a>
        <h3>{}</h3>
        <a href="{}">Buy on opensea!</h1>
        '''.format(tokenId,data['imgURL'],data['tokenURI'],data['claimed'],data['openseaUrl'],)
    else:
        return '''
        <h1>Crypto Bull #{}</h1>
        <img src="{}" height="150" width="150" ></img>
        </br>
        </br>
        <a href="{}">Traits</a>
        <h3>{}</h3>
        <a href="{}">Buy on opensea!</h1>
        '''.format("-/-","","","Whoops.. try again","",)
        
        
if __name__ == "__main__":
    #app.run() <- Use this in production
    app.run(host="10.0.0.17") # Your local IP
