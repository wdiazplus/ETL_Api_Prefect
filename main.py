import requests
from prefect import task, Flow

@task(log_stdout=True)
def extract():
   response = requests.get("https://jsonplaceholder.typicode.com/posts") 
   print(f"STATUS: {response.status_code}")
   response = response.json()
   return response

@task(log_stdout=True)
def load(response):
   output = response[1]["title"]
   print(output)


with Flow("ETL-JsonPlaceHolder API") as flow:
    raw = extract()
    load(raw)
    
flow.run()