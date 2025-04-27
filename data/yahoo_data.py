import requests                  # [handles the http interactions](http://docs.python-requests.org/en/master/) 
from bs4 import BeautifulSoup    # beautiful soup handles the html to text conversion and more
import re                        # regular expressions are necessary for finding the crumb (more on crumbs later)
from datetime import datetime    # string to datetime object conversion
from time import mktime          # mktime transforms datetime objects to unix timestamps
import json
import os
import pymysql



def websiteSoup(stock):
    """
    get crumb and cookies for historical data csv download from yahoo finance

    parameters: stock - short-handle identifier of the company 
    
    returns a tuple of header, crumb and cookie
    """
    
    # url = 'https://finance.yahoo.com/quote/{}%3DX'.format(stock)
    url = 'https://finance.yahoo.com/quote/CNH=X/history/'
    print(url)
    with requests.session():
        header = {'Connection': 'keep-alive',
                   'Expires': '-1',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                   }
        
        website = requests.get(url, headers=header)
        soup = BeautifulSoup(website.text, 'lxml')
        with open("output.html", "w", encoding="utf-8") as file:
            file.write(str(soup))
    
    return str(soup)

def pattern_data(soup,regex_patterns):

    rp = regex_patterns
    html_text = soup
    

    pattern_usdcnh = rp.get("pattern_usdcnh")
    pattern_symbol = rp.get("pattern_symbol")
    pattern_time = rp.get("pattern_time")
    pattern_price = rp.get("pattern_price")
    pattern_change = rp.get("pattern_change")
    pattern_change_percent = rp.get("pattern_change_percent")

    # 0. Extract the JSON block for symbol "CNH=X" using pattern_usdcnh.
    usdcnh_match = re.search(pattern_usdcnh, soup, re.DOTALL)
    if usdcnh_match:
        usdcnh_text = usdcnh_match.group(0)
        print("Extracted JSON block:")
        # print(usdcnh_text)

        # checkin the symbol 
        symbol_match = re.search(pattern_symbol,usdcnh_text,re.DOTALL).group(0).replace("\\","")
        print(symbol_match)

        # 1. Now extract time data from the extracted text.
        time_match = re.search(pattern_time,usdcnh_text, re.DOTALL).group(0).replace("\\","")
        # .group(0).replace("\\","") this part code is to remove the \ in the result
        if time_match:
            json_str = "{" + time_match + "}"
            data = json.loads(json_str)
            raw_time = data['regularMarketTime']['raw']
            fmt_time = data['regularMarketTime']['fmt']
            print("regularMarketTime -> raw:", raw_time, ", fmt:", fmt_time)

        # 2. Now extract price data from the extracted text.
        price_match = re.search(pattern_price, usdcnh_text, re.DOTALL).group(0).replace("\\","") 
        if price_match:
            json_str = "{" + price_match + "}"
            data = json.loads(json_str)
            raw_price = data['regularMarketPrice']['raw']
            fmt_price = data['regularMarketPrice']['fmt']
            print("regularMarketPrice -> raw:", raw_price, ", fmt:", fmt_price)
        else:
            print("regularMarketPrice not found.")


        # Extract change data.
        change_match = re.search(pattern_change, usdcnh_text, re.DOTALL).group(0).replace("\\","") 
        if change_match:
            # print(change_match)
            json_str = "{" + change_match + "}"
            data = json.loads(json_str)
            raw_change = data['regularMarketChange']['raw']
            fmt_change = data['regularMarketChange']['fmt']
            print("regularMarketChange -> raw:", raw_change, ", fmt:", fmt_change)
        else:
            print("regularMarketChange not found.")

        # Extract change percent data.
        change_percent_match = re.search(pattern_change_percent, usdcnh_text, re.DOTALL).group(0).replace("\\","") 
        if change_percent_match:
            # print(change_percent_match)
            json_str = "{" + change_percent_match + "}"
            data = json.loads(json_str)
            raw_change_percent = data['regularMarketChangePercent']['raw']
            fmt_change_percent = data['regularMarketChangePercent']['fmt'].replace('%','')
            print("regularMarketChangePercent -> raw:", raw_change_percent, ", fmt:", fmt_change_percent)
        else:
            print("regularMarketChangePercent not found.")
    else:
        print("USDCNH JSON block not found.")
    
    return {
        "symbol": "CNH=X",
        "rawMarketTime": raw_time,
        "fmtMarketTime": fmt_time,
        "rawMarketPrice": float(raw_price),
        "fmtMarketPrice": float(fmt_price),
        "rawMarketChange": float(raw_change),
        "fmtMarketChange": float(fmt_change),
        "rawMarketChangePercent": float(raw_change_percent),
        "fmtMarketChangePercent": float(fmt_change_percent)
    }


def save_to_mysql(data_dict, table_name="market_data"):
    """
    Save parsed market data to a MySQL table.
    
    Parameters:
        data_dict: dict with keys:
            symbol, rawMarketTime, fmtMarketTime, rawMarketPrice, fmtMarketPrice,
            rawMarketChange, fmtMarketChange, rawMarketChangePercent, fmtMarketChangePercent
        table_name: str
    """
    # Define MySQL connection details
    conn = pymysql.connect(
        host='10.0.0.3',
        port=3306,
        user='root',
        password='142857wyss',
        database='longproserh',
        charset='utf8mb4'
    )

    insert_sql = f"""
    INSERT INTO {table_name} (
        symbol, 
        rawMarketTime, 
        fmtMarketTime, 
        rawMarketPrice, 
        fmtMarketPrice, 
        rawMarketChange, 
        fmtMarketChange, 
        rawMarketChangePercent, 
        fmtMarketChangePercent
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                insert_sql,
                (
                    data_dict["rawMarketTime"],
                    data_dict["fmtMarketTime"],
                    data_dict["rawMarketPrice"],
                    data_dict["fmtMarketPrice"],
                    data_dict["rawMarketChange"],
                    data_dict["fmtMarketChange"],
                    data_dict["rawMarketChangePercent"],
                    data_dict["fmtMarketChangePercent"]
                )
            )
        conn.commit()
        print("✅ Data inserted successfully into MySQL.")
    except Exception as e:
        print("❌ Failed to insert data into MySQL:", e)
    finally:
        conn.close()



if __name__ == "__main__":


    regex_patterns = {
    "pattern_usdcnh": "<script\\s+data-sveltekit-fetched=\"\"\\s+data-ttl=\"1\"[\\s\\S]*?<\\/script>", 
    "pattern_symbol": "\\\\\"symbol\\\\\":\\\\\".*?\\\\\"",
    "pattern_time" : "\\\\\"regularMarketTime\\\\\":\\{.*?\\}",
    "pattern_price": "\\\\\"regularMarketPrice\\\\\":\\{.*?\\}",
    "pattern_change": "\\\\\"regularMarketChange\\\\\":\\{.*?\\}",
    "pattern_change_percent": "\\\\\"regularMarketChangePercent\\\\\":\\{.*?\\}"
    }

    soup = websiteSoup('CNH=X')
    result_dic = pattern_data(soup,regex_patterns)

    # print(result_dic)

    save_to_mysql(result_dic)
    