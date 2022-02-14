import requests
import json
import urllib3
import sys
import os 

from flask import Flask, render_template,  send_from_directory

app = Flask(__name__ , static_url_path='/static')

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
    claimed=True
    if(response_dict["result"] == "0x0000000000000000000000000000000000000000000000000000000000000000"):
        claimed = False
    resp={
        'openseaUrl': 'https://opensea.io/assets/0x469823c7b84264d1bafbcd6010e9cdf1cac305a3/' + str(bullTokenIdDec),
        'tokenURI': "https://www.cryptobullsociety.com/metadata/" + str(bullTokenIdDec) + ".json",
        'imgURL': 'https://cryptobullsociety.com/images/'+str(bullTokenIdDec)+'.png',
        'claimed': claimed
        }
    return resp


def renderPage(tokenId,openseaUrl,imgUrl,claimed):
    claimedColor="C9FBA0"
    claimedColorHover="72ae7f"
    claimedText="Not claimed 🥳"
    if claimed == True:
        claimedColor="FF8A80"
        claimedText="Claimed 🐻"
        claimedColorHover="D50000"
    return render_template("index.html",tokenId=tokenId,openseaUrl=openseaUrl,imageUrl=imgUrl,claimedColor=claimedColor,claimedText=claimedText,claimedColorHover=claimedColorHover)

@app.route('/')
def firstRoute():
    data=isBearClaimed(1383)
    return renderPage(1383,data['openseaUrl'],data['imgURL'],data['claimed'])
        
# index
@app.route('/<int:tokenId>')
def index(tokenId):
    if tokenId <= 7777 and tokenId > 0: 
        data=isBearClaimed(tokenId)
        return renderPage(tokenId,data['openseaUrl'],data['imgURL'],data['claimed'])
    else:
        return renderPage(1383,"https://opensea.io/assets/0x469823c7b84264d1bafbcd6010e9cdf1cac305a3/1383","https://cryptobullsociety.com/images/1383.png",False)
        
        
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) #<- Use this in production
    #app.run(host="10.0.0.17") # Your local IP
