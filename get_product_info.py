from urllib.request import urlopen 
import pandas as pd
import numpy as np
import time
import json
from supabase import create_client, Client

url = "https://ikgavjfgczjrpgbvaaml.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlrZ2F2amZnY3pqcnBnYnZhYW1sIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTcyOTAzNzMsImV4cCI6MjAxMjg2NjM3M30.361A1KSZloriFgthC0Xh67brucqeMLu0Y7qMlj566XU"
supabase = create_client(supabase_url = url,supabase_key= key)


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
        product["name"] = item["name"] #
        product["stock"] = item["stock"]
        product["sold"] = item["sold"]
        product["historical_sold"] = item["historical_sold"]
        product["liked_count"] = item["liked_count"]
        product["brand"] = item["brand"]#
        product["price"] = item["price"]
        product["price_min"] = item["price_min"]
        product["price_max"] = item["price_max"]
        product["discount"] = item["raw_discount"]
        product["rating_star"] = item["item_rating"]["rating_star"]
        product["rating_count_total"] = item["item_rating"]["rating_count"][0]
        product["rating_count_1"] = item["item_rating"]["rating_count"][1]
        product["rating_count_2"] = item["item_rating"]["rating_count"][2]
        product["rating_count_3"] = item["item_rating"]["rating_count"][3]
        product["rating_count_4"] = item["item_rating"]["rating_count"][4]
        product["rating_count_5"] = item["item_rating"]["rating_count"][5]
        product["rcount_with_image"] = item["item_rating"]["rcount_with_image"]
        product["rcount_with_context"] = item["item_rating"]["rcount_with_context"]
        product["shop_location"] = item["shop_location"]#
        product["crawed_time"] = time.time()
        products.append(product)
    return products

df_shop = pd.read_csv("shop_id.csv")

products = []
for shop_id in df_shop["id"]:
    products += get_shop_products(shop_id)

detail_df = pd.read_csv("product_detail.csv")

df_products = pd.DataFrame.from_dict(products)
df_new_product = df_products[~df_products['item_id'].isin(detail_df['item_id'])]

detail_df_new = pd.concat([detail_df, df_new_product])
detail_df_new.to_csv('product_detail.csv', index=False)
if not df_new_product.empty:
    detail_df_new.to_csv('product_detail.csv', index=False)
    data = df_new_product.to_dict(orient="records")
    result = supabase.table("sanpham").upsert(data).execute()
try:
    df_products = df_products.drop(columns = ["name", "brand", "shop_location"])
except:
    pass
named_tuple = time.localtime() # lấy struct_time
time_string = time.strftime("%m_%d_%Y", named_tuple)
df_products.to_csv(f'./data/product_info_{time_string}.csv', mode='a', index=False, header = False)
data = df_products.to_dict(orient="records")
result = supabase.table("CT_sanpham").insert(data).execute()