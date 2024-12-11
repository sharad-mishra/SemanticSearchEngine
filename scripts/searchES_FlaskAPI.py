from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import tensorflow_hub as hub
import tensorflow as tf
import sys

app = Flask(__name__, static_folder='static', template_folder='../templates')
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def connect2ES():
    if es.ping():
        print('Connected to ES!')
    else:
        print('Could not connect!')
        sys.exit()
    print("*********************************************************************************")
    return es

def keywordSearch(es, q):
    b = {
        'query': {
            'match': {
                "title": q
            }
        }
    }
    return es.search(index='questions-index', body=b)

def sentenceSimilaritybyNN(es, sent, embed):
    query_vector = embed([sent])[0].numpy().tolist()
    b = {
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'title_vector') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    }
    return es.search(index='questions-index', body=b)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    res_kw = keywordSearch(es, query)
    res_semantic = sentenceSimilaritybyNN(es, query, embed)

    kw_results = []
    semantic_results = []

    for hit in res_kw['hits']['hits']:
        kw_results.append((hit['_score'], hit['_source']['title']))

    for hit in res_semantic['hits']['hits']:
        semantic_results.append((hit['_score'], hit['_source']['title']))

    # Sort results by score within each group
    kw_results.sort(key=lambda x: x[0], reverse=True)
    semantic_results.sort(key=lambda x: x[0], reverse=True)

    return render_template('results.html', query=query, kw_results=kw_results, semantic_results=semantic_results)

@app.route('/search/<query>')
def search_api(query):
    q = query.replace("+", " ")
    res_kw = keywordSearch(es, q)
    res_semantic = sentenceSimilaritybyNN(es, q, embed)

    ret = ""
    for hit in res_kw['hits']['hits']:
        ret += f"KW: {hit['_score']}\t{hit['_source']['title']}\n"

    for hit in res_semantic['hits']['hits']:
        ret += f"Semantic: {hit['_score']}\t{hit['_source']['title']}\n"

    return ret

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)