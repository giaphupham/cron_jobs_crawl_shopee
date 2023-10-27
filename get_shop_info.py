import time
import pandas as pd
import json
from urllib.request import urlopen
from supabase import create_client, Client

url = "https://ikgavjfgczjrpgbvaaml.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlrZ2F2amZnY3pqcnBnYnZhYW1sIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTcyOTAzNzMsImV4cCI6MjAxMjg2NjM3M30.361A1KSZloriFgthC0Xh67brucqeMLu0Y7qMlj566XU"
supabase = create_client(supabase_url = url,supabase_key= key)

def get_shop_info(shop_id):

    api_url = f'https://shopee.vn/api/v4/product/get_shop_info?shopid={shop_id}'
  #  print(api_url)

    response = urlopen(api_url) 
    data_json = json.loads(response.read())
    shop_info = dict()
    shop_info["id"] = data_json["data"]["shopid"]
    shop_info["username"] = data_json["data"]["account"]["username"]
    shop_info["rating_star"] = data_json["data"]["rating_star"]
    shop_info["rating_bad"] = data_json["data"]["rating_bad"]
    shop_info["rating_good"] = data_json["data"]["rating_good"]
    shop_info["rating_normal"] = data_json["data"]["rating_normal"]
    shop_info["item_count"] = data_json["data"]["item_count"]
    shop_info["follower_count"] = data_json["data"]["follower_count"]
    shop_info["place"] = data_json["data"]["place"]
    shop_info["response_rate"] = data_json["data"]["response_rate"]
    shop_info["response_time"] = data_json["data"]["response_time"]
    shop_info["create_time"] = data_json["data"]["ctime"]
    shop_info["crawled_time"] = time.time()

    return shop_info

shops_info = []
df_shop = pd.read_csv("shop_id.csv")

for shop_id in df_shop["id"]:
    shop_info = get_shop_info(shop_id)
    shops_info.append(shop_info)

df_shop_info = pd.DataFrame.from_dict(shops_info)

df_shop_info.to_csv(f"./data/shop_info_{time.time()}.csv", mode = 'a', index = False, header = False)
result = supabase.table("CT_shop").insert(shops_info).execute()

