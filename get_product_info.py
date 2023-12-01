import requests
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
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept-Language': 'en,vi;q=0.9,vi-VN;q=0.8,fr-FR;q=0.7,fr;q=0.6,en-US;q=0.5',
         'Sec-Fetch-Dest':'document',
         'Sec-Fetch-Mode':'navigate',
         'Sec-Fetch-Site':'cross-site',
         'Sec-Fetch-User':'?1',
         'Sec-Ch-Ua-Platform':'"Windows"',
         'Sec-Ch-Ua':'"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'}

    cookies = {
        'SPC_F':'yi14NQEfv4uEk57a9j743vDYiDdLQnlq',
        'REC_T_ID':'8e128935-b769-11ed-8bd4-2aec15cc3bd7',
        '_fbp':'fb.1.1677589950417.661269238',
        'SPC_CLIENTID':'eWkxNE5RRWZ2NHVFhmyqqmzazighbhvs',
        '_hjSessionUser_868286':'eyJpZCI6IjU4Njc4YjlkLWE2OTctNWMwMS05M2MwLTA2MDQ3ZjY4MzFlNCIsImNyZWF0ZWQiOjE2Nzc1ODk5NTMyNjEsImV4aXN0aW5nIjp0cnVlfQ==',
        'language':'en',
        '_gcl_au':'1.1.170436240.1694226140',
        '_ga_RLCQNPT3EM':'GS1.1.1696169631.1.1.1696169794.58.0.0',
        'SC_DFP':'JdqZfxPCpvCpSufPeyNdXhmoNKHElNiq',
        '_ga_M32T05RVZT':'GS1.1.1698247094.71.0.1698247094.60.0.0',
        '_ga_3XVGTY3603':'GS1.1.1698287263.4.1.1698287347.60.0.0',
        '_ga':'GA1.2.1063866165.1677589952',
        'SPC_SI':'cbVlZQAAAABvWnEwWHp4N9HgPQAAAAAAbVdvMEZEWkc=',
        'SPC_SEC_SI':'v1-bUdwenNYbktud3Y2UG5LM6Ig6ENqbiagSHYIDNKiP3867RbqjickSTP5oq0TVamgzaWqMS9pa8jin/Bt3jnA9Yzf2dUq/QQ6scqPsObPNl8=',
        '_QPWSDCXHZQA':'d0dde1d2-61c2-4914-a4eb-584894006a1c',
        'REC7iLP4Q':'038154af-f84a-4b61-b268-b8a628674467',
        'SPC_ST':'.TEI1Q2c0MFFGeWIzUXZXenUmQsdgiHu9YprxKbqCVViLCqVoaZX22CSumpaxp1Lqx36UwTGRIoXJCfgK3+sz+GRIGX6XqNN+Ca0YETXKlds8ESFJWLSh+DQ7sU2VIe9i9GZMbyyPRm6j21XlQagexYXYW2o8IDIK7n1iHLSreLhEJPFnecSHMNUoDzvNvbMRhU9dZm0M3p5nbC4MZzveHg==',
        'SPC_U':'170557637',
        'SPC_R_T_ID':'hEC3RbzJcbzhKrF9l/lWv9r2RQD0TwwZqFB7nXGaEsaff9IBFecbRipBj05G5YKocitapxmtRwRMgcROuaLQzcy1RPzjVXPkLEbScUGDa2Gg/+htwt75uxvMW6IgU1RRrmZTBXYUBruqbibgCZmAplI4NkezgX4pKi6HGCNNd/g=',
        'SPC_R_T_IV':'UTdQVmFodXYzWkt5a0VScw==',
        'SPC_T_ID':'hEC3RbzJcbzhKrF9l/lWv9r2RQD0TwwZqFB7nXGaEsaff9IBFecbRipBj05G5YKocitapxmtRwRMgcROuaLQzcy1RPzjVXPkLEbScUGDa2Gg/+htwt75uxvMW6IgU1RRrmZTBXYUBruqbibgCZmAplI4NkezgX4pKi6HGCNNd/g',
        'SPC_T_IV':'UTdQVmFodXYzWkt5a0VScw==',
        'shopee_webUnique_ccd':'ktVMZidId7WnpVXGoNaY7Q%3D%3D%7CD3dPR4FPFt9p7d2jhxzBTuN1FQrJUBE0RJOvUxuPXvxWwZIXKrGTcc1OPZovCpylaU02z29D%2BZ46bA%3D%3D%7C6AshV7sk5ngDeLnE%7C08%7C3',
        'ds':'4f5a3e8e358540e80885e0247da248c7',
        'SPC_EC':'d25NbjBBdENpaWYzVkN4TnQZKE5yV/BHuDkJ6+iBWWZOOVs/CPL5UhbLjVYDLWifnyGKyCKWUXJT3Tv4IzmQZplRvgniy93AA6fyfgIleIWxNoKlHlKaXZwjHEmX4nI5EqDv/k8bLkc0PxjOWhDga++He9Dw98q0URDy62DXLZg='
    }

    params = {
        'limit': '99999',
        'offset': '0'
    }

    response = requests.get(api_url, headers=headers, params=params, cookies=cookies)
    
    if response.status_code == 200:
        data_json = json.loads(response.content) 
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
    else:
        return []

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