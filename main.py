from fastapi import FastAPI
import httpx
import asyncio

app = FastAPI()
ceny = {}

async def fetch():
    while True:
        async with httpx.AsyncClient() as client:
            r1 = await client.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=eur")
            r2 = await client.get("https://query1.finance.yahoo.com/v7/finance/quote?symbols=TSLA,AAPL,^GSPC")

            if r1.status_code == 200:
                ceny['BTC'] = r1.json()['bitcoin']['eur']
                ceny['ETH'] = r1.json()['ethereum']['eur']
            if r2.status_code == 200:
                quotes = r2.json()['quoteResponse']['result']
                ceny['TSLA'] = next(q['regularMarketPrice'] for q in quotes if q['symbol'] == 'TSLA')
                ceny['AAPL'] = next(q['regularMarketPrice'] for q in quotes if q['symbol'] == 'AAPL')
                ceny['SP500'] = next(q['regularMarketPrice'] for q in quotes if q['symbol'] == '^GSPC')
        await asyncio.sleep(1)

@app.get("/ceny")
async def get_ceny():
    return ceny

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(fetch())
