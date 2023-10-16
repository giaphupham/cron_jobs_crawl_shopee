from urllib.request import urlopen 
import pandas as pd
import numpy as np
import time
import json

def get_shop_products(shop_id):
    api_url = f'https://shopee.vn/api/v4/recommend/recommend?bundle=shop_page_product_tab_main&limit=99999&offset=0&shopid={shop_id}'
    products = []
    
    response = urlopen(api_url) 
    data_json = json.loads(response.read()) 
    #print(data_json["data"]["sections"][0])
    for item in data_json["data"]["sections"][0]["data"]["item"]:
        product = dict()
        product["item_id"] = item["itemid"]
        product["shop_id"] = item["shopid"]
        product["stock"] = item["stock"]
        product["sold"] = item["sold"]
        product["historical_sold"] = item["historical_sold"]
        product["liked_count"] = item["liked_count"]
        product["price"] = item["price"]
        product["price_min"] = item["price_min"]
        product["price_max"] = item["price_max"]
        product["discount"] = item["raw_discount"]
        product["rating_star"] = item["item_rating"]["rating_star"]
        product["rating_count_total"] = item["item_rating"]["rating_count"][0]
        product["rating_count"] = item["item_rating"]["rating_count"]
        product["rcount_with_image"] = item["item_rating"]["rcount_with_image"]
        product["rcount_with_context"] = item["item_rating"]["rcount_with_context"]
        product["crawed_time"] = time.time()
        products.append(product)
    return products

df_shop = pd.read_csv("shop_id.csv")


products = []
for shop_id in df_shop["id"]:
    products += get_shop_products(shop_id)
    
df_products = pd.DataFrame.from_dict(products)

df_products.to_csv('product_info.csv', mode='a', index=False, header = False)

    