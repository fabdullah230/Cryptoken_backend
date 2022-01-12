import requests

def getPrice(token):

    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids="+token+"&vs_currencies=usd").json()
    except Exception as e:
        return 0
    #print(response[token]['usd'])
    return response[token]['usd']
















if __name__ == "__main__":
    getPrice("bitcoin")