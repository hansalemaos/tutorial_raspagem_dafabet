import re
from time import sleep
import bs4
from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from PrettyColorPrinter import add_printer

add_printer(1)


def obter_dataframe(query="*"):
    df = pd.DataFrame()
    while df.empty:
        df = get_df(
            driver,
            By,
            WebDriverWait,
            expected_conditions,
            queryselector=query,
            with_methods=True,
        )
    return df


driver = Driver(uc=True)
sleep(5)
driver.get('https://www.dafabet.com/pt/dfgoal/sports/240-football/22977-brazil')
sleep(5)
while True:
    try:
        df = obter_dataframe(query="div.event-component")
        df = df.aa_innerHTML.apply(bs4.BeautifulSoup).apply( lambda soup: [x.text.strip() for x in soup.find_all('a', {'class': 'opponent-name'})] + [x.text.strip() for x in soup.find_all('span', {'class': 'formatted_price'})]).apply( lambda x: x if all([re.match(r'^\d+\.\d+$', y) for y in x[3:]]) else pd.NA ).dropna().apply(pd.Series).rename(columns={0: 'team1_nome', 1: 'team2_nome' , 2: 'team1', 3: 'empate', 4: 'team2'} ).astype( {'team1': 'Float64', 'empate': 'Float64', 'team2': 'Float64'}).reset_index(drop=True)
        print(df)
        sleep(5)
    except Exception as e:
        print(e)
        sleep(2)
