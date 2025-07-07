import pandas as pd
import requests
import time
import os
import random

from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")


# Read booklist.csv
df = pd.read_csv('output.csv')
random_index = random.randint(0, len(df) - 1)
title = df.loc[random_index, 'title']
image_url = df['image link']

#create a media container
create_url = f'https://graph.facebook.com/v19.0/{IG_USER_ID}/media'
create_payload = {
    'image_url': 'https:'+ image_url,
    'caption': 'book title: '+ title + "\\nAlison has built a bot that posts books to Instagram! This is a test post done with the Insta api and Python, weeeeee!",
    'access_token': ACCESS_TOKEN
}
create_res = requests.post(create_url, data=create_payload)
create_res_json = create_res.json()

#debugging notice
if 'id' not in create_res_json:
    raise Exception(f"Error creating media container: {create_res_json}")

creation_id = create_res_json['id']
print("Media container created:", creation_id)

# set sleep time
time.sleep(3)

# publish the media container
publish_url = f'https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish'
publish_payload = {
    'creation_id': creation_id,
    'access_token': ACCESS_TOKEN
}
publish_res = requests.post(publish_url, data=publish_payload)
publish_res_json = publish_res.json()

#debugging notice
if 'id' not in publish_res_json:
    raise Exception(f"Error publishing media: {publish_res_json}")

print("Post published successfully. ID:", publish_res_json['id'])
