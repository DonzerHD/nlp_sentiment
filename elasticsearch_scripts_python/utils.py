from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

def index_document(document):
    """
    Indexes the given document in Elasticsearch.
    
    Args:
        document (dict): The document to be indexed.
    """
    es.index(index="notes", body=document)