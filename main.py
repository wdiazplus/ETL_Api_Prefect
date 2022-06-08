import requests
import datetime
from prefect import task, Flow
import json


@task(log_stdout=True, max_retries=3, retry_delay=datetime.timedelta(seconds=10) )
def extract(id):
   raw = requests.get(f"https://jsonplaceholder.typicode.com/posts/{id}") 
   print(f"STATUS: {raw.status_code}")
   raw = json.loads(raw.text)
   with open('./raw.json','w', encoding='utf-8') as file:
       json.dump(raw, file, ensure_ascii=False, indent=4)    
   return raw 


@task(log_stdout=True, max_retries=3, retry_delay=datetime.timedelta(seconds=10))
def transform(raw):
   transform = raw["title"]
   with open('./transform.json','w', encoding='utf-8') as file:
       json.dump(transform, file, ensure_ascii=False, indent=4) 
   return transform


@task(log_stdout=True, max_retries=3, retry_delay=datetime.timedelta(seconds=10))
def load(transform):
    print(str(transform))

   
with Flow("ETL-JsonPlaceHolder API") as flow:
    raw = extract(10)
    transform = transform(raw)
    load(transform)

    
flow.run()