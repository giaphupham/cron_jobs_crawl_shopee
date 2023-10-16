import time
import pandas as pd
import json
from urllib.request import urlopen 
from datetime import datetime
now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def get_shop_info(url):
    url = url.strip()
    shop_name = url.split('/')[-1]
    api_url = f'https://shopee.vn/api/v4/shop/get_shop_detail?username={shop_name}'
    response = urlopen(api_url) 
    data_json = json.loads(response.read()) 
    shop_info = dict()
    shop_info["id"] = data_json["data"]["shopid"]
    shop_info["rating_star"] = data_json["data"]["rating_star"]
    shop_info["rating_bad"] = data_json["data"]["rating_bad"]
    shop_info["rating_good"] = data_json["data"]["rating_good"]
    shop_info["rating_normal"] = data_json["data"]["rating_normal"]
    shop_info["item_count"] = data_json["data"]["item_count"]
    shop_info["follower_count"] = data_json["data"]["follower_count"]
    shop_info["following_count"] = data_json["data"]["account"]["following_count"]
    shop_info["has_flash_sale"] = data_json["data"]["has_flash_sale"]
    shop_info["has_shopee_flash_sale"] = data_json["data"]["has_shopee_flash_sale"]
    shop_info["has_in_shop_flash_sale"] = data_json["data"]["has_in_shop_flash_sale"]
    shop_info["has_brand_sale"] = data_json["data"]["has_brand_sale"]
    shop_info["crawled_time"] = time.time()

    return shop_info

shops_info = []
df_shop = pd.read_csv("shop_id.csv")

for shop_url in df_shop["shop_url"]:
    shop_info = get_shop_info(shop_url)
    shops_info.append(shop_info)

df_shop_info = pd.DataFrame.from_dict(shops_info)

df_shop_info.to_csv(f"./data/shop_info_{now}.csv", mode = 'a', index = False, header = False)