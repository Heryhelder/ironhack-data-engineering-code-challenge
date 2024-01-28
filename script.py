import asyncio
import requests

async def fetchCryptoHistoricalData(asset_base, asset_quote='USD'):
    # TODO: Add your own API key
    API_KEY = ''

    URL = 'https://rest.coinapi.io/v1/exchangerate/{asset_base}/{asset_quote}/history?period_id=1DAY&time_start=2016-01-01T00:00:00&limit=360'.format(asset_base=asset_base, asset_quote=asset_quote)

    HEADERS = {
        'Accept': 'text/plain',
        'X-CoinAPI-Key': API_KEY
    }

    try:
        response = requests.get(URL, headers=HEADERS)
        
        if response.status_code == 200:
            print(response.json())
        else:
            raise requests.HTTPError(response.status_code, response.text)
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

async def main():
    cryptos = {
        'bitcoin': 'BTC',
        'ethereum': 'ETH',
        'ripple': 'XRP',
        'litecoin': 'LTC',
        'stellar': 'XLM'
    }

    print('Choose crypto:')
    print('Bitcoin')
    print('Ethereum')
    print('Ripple')
    print('Litecoin')
    print('Stellar')

    crypto_choice = input().lower()
    
    if crypto_choice not in cryptos.keys():
        print('Invalid choice. Exiting...')
        exit()

    asset_base = cryptos[crypto_choice]

    await fetchCryptoHistoricalData(asset_base)

if __name__ == '__main__':
    asyncio.run(main())