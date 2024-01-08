from sys import argv
from datetime import datetime, timedelta
import platform
import aiohttp
import asyncio
import logging


cur_lst = ['AUD', 'AZN', 'BYN', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 'GEL',
           'HUF', 'ILS', 'JPY', 'KZT', 'MDL', 'NOK', 'PLN', 'SEK', 'SGD', 'TMT', 'TRY',
           'UAH', 'USD', 'UZS', 'XAU']


logger = logging.getLogger('log')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

fh = logging.FileHandler("script.log")
fh.setLevel(logging.ERROR)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)


async def ex_rate_take(session, date, cur):
    url = "https://api.privatbank.ua/p24api/exchange_rates?date="
    try:
        async with session.get(f'{url}{date}') as response:
            if response.status == 200:
                res = await response.json()
                return nec_cur(res, cur)
            logger.error(f"Error status: {response.status} for {url}{date}")
            # return f"Error status: {response.status} for {url}{date}"
    except aiohttp.ClientConnectorError as err:
        logger.error(f'Connection error: {url}', str(err))
        # return f'Connection error: {url}', str(err)


def nec_cur(resp, cur):
    cur_dict = {resp["date"]: {}}
    check_dict = {}
    for i in resp["exchangeRate"]:
        if i["currency"] in cur:
            check_dict[i["currency"]] = {"sale": i["saleRateNB"], "purchase": i["purchaseRateNB"]}
    for i in cur:
        cur_dict[resp["date"]][i] = check_dict[i]
    return cur_dict


def dates_handler(days):
    res_dates = []
    now = datetime.now()
    td = timedelta(days=1)
    for i in range(int(days)):
        res_dates.append(now.strftime("%d.%m.%Y"))
        now = now - td
    return res_dates


async def main():
    coro = []
    days, cur = argv[1], argv[2:]
    if cur:
        for i in cur:
            if i not in cur_lst:
                logger.debug(f"There is no such exchange rate for this currency: {i}")
                cur.remove(i)
    else:
        cur = ["USD", "EUR"]
    if int(days) > 10:
        logger.debug("The maximum period for viewing the exchange rate is 10 days")
    dates = dates_handler(days)
    async with aiohttp.ClientSession() as session:
        for date in dates:
            coro.append(ex_rate_take(session, date, cur))
        res = asyncio.gather(*coro)
        return await res


def con_main():
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    res = asyncio.run(main())
    for y in res:
        print(y)


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = asyncio.run(main())
    for r in result:
        print(r)
