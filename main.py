import requests
from prefect import task, Flow

@task
def extract():
   response = requests.get("https://jsonplaceholder.typicode.com/posts") 
   response = response.json()
   return response
@task
def load(response):
   output = response[1]["title"]
   print(output)


with Flow("ETL-JSONPlaceHolder API") as flow:
    raw = extract()
    load(raw)
    
flow.run()