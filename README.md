#  CryptoBull-Claim-Check

Python web app Proof of concept, API that checks whether a certian Crypto Bull Society's Bull has claimed its Crypto Bear

Demo: https://cryptobull-claim-server.herokuapp.com/7777

<img src="https://github.com/edenbd50/CryptoBull-Claim-Check/blob/main/images/demo_v2.webp" alt="demo_webp" >
	

<a href="https://www.buymeacoffee.com/peterpen5100" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>


	
## Table of Contents

<!-- MarkdownTOC -->
0. [Understanding the contract](#0.understandingthecontract)
1. [cURL request](#curlrequest)
2. [Configuration](#configuration)
3. [Requirements](#requirements)
4. [Setup project](#setupproject)
5. [Deploy your own](#deployyourown)
<!-- /MarkdownTOC -->

## 0. Understanding the contract

I have seen in the Discord group that there is a common problem for Bull buyers:</br>
`How do I know whether a certian bull has claimed his bear?`.</br>
Most of the responds were you can do it manually by:</br>
- `Step 1:` browsing into the Bull's Opensea page</br>
- `Step 2:` Navigate to the owner's page</br>
- `Step 3:` Copy owner's wallet</br>
- `Step 4:` Open EtherScan website, search for the `Claim bear`</br>
</br>
The problem with this approach is that it takes time and the bull might have been transfered post claim,</br>
in that case you would have to look into every one that has held that bull in the past, again, Manually which brings your back to Step 2.</br>


Therefore, I took the challenge to make an Automation script for that process (Little did I know that it would be much easier than I thought).</br>

### My process began with manual process Following Bull number [#7777](https://opensea.io/assets/0x469823c7b84264d1bafbcd6010e9cdf1cac305a3/7777)</br>


<img src="https://github.com/edenbd50/CryptoBull-Claim-Check/blob/main/images/bull_number_7777.png" alt="bull#777_img" >
 
Owned by 0xLem

<img src="https://github.com/edenbd50/CryptoBull-Claim-Check/blob/main/images/lem_page.png" alt="lem_page" >

Followed his wallet contracts and lucky me, he claimed his bear!

<img src="https://github.com/edenbd50/CryptoBull-Claim-Check/blob/main/images/etherscan_claim_bear.png" alt="etherscan_claim_bear" >

From there I've found the CryptoClaim Contract written in Solidity (The programming language)
Now we can access the contract and see what kind of functions we have there

<img src="https://github.com/edenbd50/CryptoBull-Claim-Check/blob/main/images/etherscan_contract_functions.png" alt="etherscan_contract_functions" > 

I've highlighted the relevent parts:

- The `Wallet Address` in the URL

- The `Contract` Tab which will show us the Contract code.

- The `Read Contract`  tab which shows the public functions.


And we found our function !!

`4. hasBullClaimed`, I've entered the bull's Id `7777` and hoped for the best, I got in response: `1` which I could guessed that it is claimed, then I tried with my own bull that did not claimed and it returned `0` so it safe to say that whats the function does.

Just to be sure I've jumped into the `Code` tab, searched for the function's name inside the `CryptoBearsClaim.sol` (needed to expand the code in the icon on the right)

<img src="https://github.com/edenbd50/CryptoBull-Claim-Check/blob/main/images/has_bull_claimed_solidity.png" alt="has_bull_claimed" > 

And there it is, thanks for the great developers that actually documanted the code we can understand that:

`0 = False, not claimed`

`1 = True, claimed`



From here I've just scraped the web request from the Contract:

- Entered DevTools -> Network -> Cleared any other requests.

- Pressed the `Query` buttton

- New network request to the SmartContract block has dispatched

- Looking into the Response to verify that it is my response.

- Copy the request as cUrl


<img src="https://github.com/edenbd50/CryptoBull-Claim-Check/blob/main/images/scraping_process.png" alt="scraping_process" > 


## 1 cUrl Request
```
curl "https://node1.web3api.com/" -X POST -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0" 
-H "Accept: */*" -H "Accept-Language: en-GB,en;q=0.5" 
-H "Accept-Encoding: gzip, deflate, br" 
-H "Referer: https://etherscan.io/"
-H "Content-Type: application/json"
-H "Origin: https://etherscan.io" 
-H "Connection: keep-alive" 
-H "Sec-Fetch-Dest: empty" 
-H "Sec-Fetch-Mode: cors" -H "Sec-Fetch-Site: cross-site" 
-H "TE: trailers" 
--data-raw "{""jsonrpc"":""2.0"",""id"":1,""method"":""eth_call"",""params"":[{
""from"":""0x0000000000000000000000000000000000000000"",
""data"":""0x45083abc0000000000000000000000000000000000000000000000000000000000001e61"",
""to"":""0x45ec819d71fcc4a2ea58ff70e66d4216c403a424""},""latest""
]}"
```


By looking at the request I've seen that the 7777 isnt located in any part of the request.. and finally realized that it is part of the data:

`0x45083abc0000000000000000000000000000000000000000000000000000000000001e61`

Only its in `Hex` not in `Dec` 

<img src="https://github.com/edenbd50/CryptoBull-Claim-Check/blob/main/images/dec_to_hex.png" alt="dec_to_hex" > 
 

Since we need to convert each time the Dec number of the Bull that we want to check if he claimed a bear, I've made an Python web app example for everyone to use. :)

  
  

## 2. Configuration
- Download [Python](https://www.python.org/downloads/release/python-380/) version `3.8.0`

## 3. Requirements
- install requirements.txt
	- `pip install -r requirements.txt` or `pip3 install -r requirements.txt`

## 4. Setup project
- Change the local ip inside app.py
	```python		
	if __name__ == "__main__":
		#app.run() <- Use this in production
		app.run(host="10.0.0.17") # Your local IP
	```
- simply run `app.py`
	- It wil display your local ip and port`
	<img src="https://github.com/edenbd50/CryptoBull-Claim-Check/blob/main/images/ip_port.png" alt="ip_port" height="100" >
 
	
- Navigate to `local_ip:port/7777`
	- Place after the slash the crypto bull that you want to use.
<img src="https://github.com/edenbd50/CryptoBull-Claim-Check/blob/main/images/claimd_his_bear_v2.png" alt="claimd_his_bear" > 


## 5. Deploy your own

- Create account in Heroku.
- Fork this repository.
- Create new Project in Heroku.
- Link your Forked project into the Heroku Project settings (Log-in with your github account to gain access to the forked project).
- Deploy 
- Press `Open app`




If you found this useful don't be shy you can always buy me a coffee as a thank you 😉☕.
<br>
<a href="https://www.buymeacoffee.com/peterpen5100" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>