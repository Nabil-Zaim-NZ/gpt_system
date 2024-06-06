import pandas as pd
from datasets import load_dataset
from elasticsearch import Elasticsearch
from flask import jsonify
from sentence_transformers import SentenceTransformer
import os

ES_INDEX = os.getenv("ES_INDEX")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL")
THRESHOLD_DOCUMENT = float(os.getenv("THRESHOLD_DOCUMENT"))

model = SentenceTransformer(MODEL)
es = Elasticsearch(ELASTICSEARCH_URL)
es.info()


def load_and_index_dataset():
    df = load_dataset("RealTimeData/bbc_news_alltime", "2024-04")["train"]
    df = pd.DataFrame(df).head(15)
    operations = [
        {"index": {"_index": ES_INDEX}}
        | {
            **row,
            "paragraph": paragraph,
            "embedding": model.encode(
                (row["title"] + " ") * 20 + (row["description"] + " ") * 5 + paragraph,
                convert_to_tensor=True,
            ).tolist(),
        }
        for i, row in df.iterrows()
        for paragraph in row["content"].split("\n\n")
        if paragraph.strip()
    ]
    es.bulk(operations=operations)


def search(request):
    query = request.json.get("query")
    if not query:
        return jsonify({"error": "Query not provided"}), 400

    query_embedding = model.encode(query, convert_to_tensor=True)

    similarity_response = es.search(
        index=ES_INDEX,
        body={
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": query_embedding.tolist()},
                    },
                }
            },
        },
    )

    keyword_response = es.search(
        index=ES_INDEX,
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^20", "description^1", "paragraph^1"],
                }
            }
        },
    )

    similarity_results = filter_results(
        [
            create_result_dict(hit, "Similarity", hit["_score"] - 1)
            for hit in similarity_response["hits"]["hits"]
            if hit["_score"] - 1 >= THRESHOLD_DOCUMENT
        ]
    )

    max_score = keyword_response["hits"]["max_score"]
    keyword_results = filter_results(
        [
            create_result_dict(hit, "Keyword", hit["_score"])
            for hit in keyword_response["hits"]["hits"]
            if hit["_score"] / max_score > THRESHOLD_DOCUMENT
        ]
    )

    return jsonify(
        {
            "similarity_results": similarity_results,
            "keyword_results": keyword_results,
        }
    )


def create_result_dict(hit, search_type, score=None):
    result_dict = {
        "_search_type": search_type,
        "title": hit["_source"]["title"],
        "description": hit["_source"]["description"],
        "link": hit["_source"].get("link", "N/A"),
        "paragraph": hit["_source"]["paragraph"],
        "content": hit["_source"]["content"],
        "top_image": hit["_source"]["top_image"],
    }
    if score is not None:
        result_dict["relevance"] = round(score, 2)
    return result_dict


def filter_results(results):
    filtered_results = {}
    for item in results:
        link = item["link"]
        if (
            link not in filtered_results
            or item["relevance"] > filtered_results[link]["relevance"]
        ):
            filtered_results[link] = item
    return list(filtered_results.values())


def get_example_questions():
    try:
        with open("static/questions.txt", "r") as file:
            questions = file.read().splitlines()
    except FileNotFoundError:
        return jsonify({"error": "questions.txt file not found"}), 404
    return jsonify({"questions": questions})


def reindex_documents():
    es.indices.delete(index=ES_INDEX, ignore_unavailable=True)
    es.indices.create(index=ES_INDEX)
    load_and_index_dataset()
    print("Documents reindexed successfully.")
