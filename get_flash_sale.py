import time
import pandas as pd
import json
from urllib.request import urlopen 

def get_flash_sale(url):
    url = url.strip()
    shop_name = url.split('/')[-1]
    api_url = f'https://shopee.vn/api/v4/shop/get_shop_detail?username={shop_name}'
    response = urlopen(api_url) 
    data_json = json.loads(response.read()) 
    print(data_json)
    has_flash_sale = data_json["data"]["has_flash_sale"]
    flash_sale_list = []
    if has_flash_sale == False:
        return []
    
    for item in data_json["data"]["priority_flash_sale_group"]["items"]:
        flash_sale = dict()
        flash_sale["promotion_id"] = item["promotion_id"]
        flash_sale["shop_id"] = item["shop_id"]
        flash_sale["item_id"] = item["item_id"]
        flash_sale["name"] = item["name"]
        flash_sale["discount"] = item["discount"]
        try:
            flash_sale["price"] = item["price"]
        except:
            flash_sale["price"] = item["hidden_price_display"]
        flash_sale["price_before_discount"] = item["price_before_discount"]
        try:
            flash_sale["flash_sale_stock"] = item["flash_sale_stock"]
        except:
            flash_sale["flash_sale_stock"] = ""
        flash_sale["is_shop_official"] = item["is_shop_official"]
        flash_sale["is_shop_preferred"] = item["is_shop_preferred"]
        flash_sale["start_time"] = item["start_time"]
        flash_sale["end_time"] = item["end_time"]
        flash_sale["crawled_time"] = time.time()
        flash_sale_list.append(flash_sale)
    
    return flash_sale_list

flash_sale_list = []

df_shop = pd.read_csv("shop_id.csv")

for shop_url in df_shop["shop_url"]:
    flash_sale = get_flash_sale(shop_url)
    flash_sale_list += flash_sale

df_flash_sale = pd.DataFrame.from_dict(flash_sale_list)

df_flash_sale.to_csv("flash_sale.csv", mode = 'a', index = False, header = False)

