from typing import Dict, Set, List, Tuple
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import csv
import os
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from query_processing import calculate_query_tfidf

from inverted_index import get_document_vector, get_weighted_inverted_index


def _get_documents_related_to_query(weighted_inverted_index: Dict[str, list], weighted_query_terms: dict) -> Set[str]:
 
    documents = set()
    inverted_index_keys = list(weighted_inverted_index.keys())
    query_keys = list(weighted_query_terms.keys())

    shared_items = [x for x in inverted_index_keys if x in query_keys]
    print("Shared items:", shared_items)

    document_count = 0
    for item in shared_items:
        for docs in weighted_inverted_index[item]:
            for doc_key in docs:
                document_count += 1
                documents.add(doc_key)
    
    
    return documents


def _get_document_vectors(documents: Set[str], dataset_name: str) -> Dict[str, Dict[str, float]]:
 
    document_vectors = {}
    for doc_id in documents:
        document_vectors[doc_id] = get_document_vector(dataset_name, doc_id)
    return document_vectors


def _get_matrix_from_documents_and_query_vectors(document_vectors: Dict[str, Dict[str, float]],
                                                 query_vector: Dict[str, float]) \
        -> Tuple[np.ndarray, np.ndarray, List[str]]:

    doc_ids = list(document_vectors.keys())
    doc_list = list(document_vectors.values())
    vectorizer = DictVectorizer()
    docs_terms_matrix = vectorizer.fit_transform(doc_list)
    query_matrix = vectorizer.transform(query_vector)
    return docs_terms_matrix, query_matrix, doc_ids


def ranking(query: str, dataset: str) -> Dict[str, float]:

    weighted_inverted_index = get_weighted_inverted_index(dataset)
    query_vector = calculate_query_tfidf(query, dataset)
    related_documents = _get_documents_related_to_query(weighted_inverted_index, query_vector)

    document_vectors = _get_document_vectors(related_documents, dataset)

    try:
        matrix, query_matrix, doc_ids = _get_matrix_from_documents_and_query_vectors(document_vectors, query_vector)
        similarity = cosine_similarity(query_matrix, matrix)
        document_ranking = dict(zip(doc_ids, similarity.flatten()))
        sorted_dict = dict(sorted(document_ranking.items(), key=lambda item: item[1], reverse=True))
        return sorted_dict
    except ValueError:
        return {}
