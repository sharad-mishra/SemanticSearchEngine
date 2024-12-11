import json
import sys
from elasticsearch import Elasticsearch

# connect to ES on localhost on port 9200
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect!')
    sys.exit()

print("*********************************************************************************");

# Define the index
b = {
    "mappings": {
        "properties": {
            "title": {
                "type": "text"
            },
            "title_vector": {
                "type": "dense_vector",
                "dims": 512
            }
        }
    }
}

ret = es.indices.create(index='questions-index', ignore=400, body=b)  # 400 caused by IndexAlreadyExistsException
print(json.dumps(ret, indent=4))

print("*********************************************************************************");