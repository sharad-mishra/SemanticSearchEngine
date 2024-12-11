import csv
import tensorflow_hub as hub
import tensorflow as tf
import elasticsearch
from elasticsearch import Elasticsearch, helpers
import sys
import os
import time
import backoff
from concurrent.futures import ThreadPoolExecutor

# Retry decorator with exponential backoff
@backoff.on_exception(backoff.expo,
                      (elasticsearch.exceptions.ConnectionTimeout,
                       elasticsearch.exceptions.ConnectionError),
                      max_tries=8)
def index_batch(es, actions):
    helpers.bulk(es, actions)

# connect to ES on localhost on port 9200 with increased timeout settings
es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=60, max_retries=10, retry_on_timeout=True)
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect!')
    sys.exit()

print("*********************************************************************************");

# Load USE4 model
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# CONSTANTS
NUM_QUESTIONS_INDEXED = 200000
BATCH_SIZE = 5000  # Increased batch size to reduce the number of bulk requests

# Col-Names: Id,OwnerUserId,CreationDate,ClosedDate,Score,Title,Body
cnt = 0
actions = []

# Verify the file path
file_path = 'c:/Users/syein/Downloads/Semantic Search Engine/semantic_search_engine/data/Questions.csv'
print(f"Attempting to open file: {file_path}")

# Check if the file exists
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    sys.exit()

start_time = time.time()

def process_row(row):
    try:
        doc_id = row[0]
        title = row[5]
        vec = tf.make_ndarray(tf.make_tensor_proto(embed([title]))).tolist()[0]

        action = {
            "_index": "questions-index",
            "_id": doc_id,
            "_source": {
                "title": title,
                "title_vector": vec,
            }
        }
        return action
    except Exception as e:
        print(f"Error processing row {cnt}: {e}")
        return None

with open(file_path, encoding='latin1') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV, None)  # skip the headers

    with ThreadPoolExecutor(max_workers=4) as executor:
        for row in readCSV:
            cnt += 1
            action = process_row(row)
            if action:
                actions.append(action)

            if cnt % BATCH_SIZE == 0:
                print(f"Indexing batch {cnt // BATCH_SIZE}...")
                executor.submit(index_batch, es, actions)
                actions = []  # Clear the batch

            if cnt == NUM_QUESTIONS_INDEXED:
                break

# Index any remaining documents
if actions:
    print("Indexing remaining documents...")
    index_batch(es, actions)

end_time = time.time()
print(f"Completed indexing {cnt} documents in {end_time - start_time} seconds.")
print("*********************************************************************************");