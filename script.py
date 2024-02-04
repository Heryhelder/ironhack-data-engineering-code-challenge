import asyncio
import requests
from sqlalchemy import create_engine
from sqlalchemy import text

async def fetch_crypto_historical_data(asset_base, asset_quote='USD'):
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
            return response.json()
        else:
            raise requests.HTTPError(response.status_code, response.text)
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

        return None
    except Exception as err:
        print(f'Other error occurred: {err}')

        return None
    
async def init_db():
    print('initializing database')
    engine = create_engine('postgresql://user:password@host:port/postgres')
    print('connection established')
    return engine

async def save_to_db(currency, data):
    if data is not None:
        engine = await init_db()
        
        with engine.begin() as conn:
            print('creating tables if not exist')
            conn.execute(text("""CREATE TABLE IF NOT EXISTS currency (
                id                SERIAL PRIMARY KEY,
                name              VARCHAR(255) NOT NULL,
                CONSTRAINT currency_unique UNIQUE (name)
            )"""))

            conn.execute(text("""CREATE TABLE IF NOT EXISTS historical (
                id                SERIAL PRIMARY KEY,
                time_period_start TIMESTAMP NOT NULL,
                time_period_end   TIMESTAMP NOT NULL,
                time_open         TIMESTAMP NOT NULL,
                time_close        TIMESTAMP NOT NULL,
                rate_open         DOUBLE PRECISION NOT NULL,
                rate_high         DOUBLE PRECISION NOT NULL,
                rate_low          DOUBLE PRECISION NOT NULL,
                rate_close        DOUBLE PRECISION NOT NULL,
                id_currency       INT NOT NULL REFERENCES currency(id),
                CONSTRAINT historical_unique UNIQUE (time_period_start, time_period_end, id_currency)
            )"""))

            print('saving data to database if not exist')
            result = conn.execute(text("INSERT INTO currency (name) VALUES (:name) ON CONFLICT ON CONSTRAINT currency_unique DO NOTHING RETURNING id"), {'name': currency})

            for row in result:
                conn.execute(text("INSERT INTO historical (time_period_start, time_period_end, time_open, time_close, rate_open, rate_high, rate_low, rate_close, id_currency) VALUES (:time_period_start, :time_period_end, :time_open, :time_close, :rate_open, :rate_high, :rate_low, :rate_close, {id_currency}) ON CONFLICT ON CONSTRAINT historical_unique DO NOTHING".format(id_currency=row.id)), data)

            print('done')

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

    # testing
    crypto_choice = input().lower()
    
    if crypto_choice not in cryptos.keys():
        print('Invalid choice. Exiting...')
        exit()

    asset_base = cryptos[crypto_choice]

    historical_data = await fetch_crypto_historical_data(asset_base)
    await save_to_db(asset_base, historical_data)

if __name__ == '__main__':
    asyncio.run(main())