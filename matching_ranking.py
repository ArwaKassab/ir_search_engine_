# from typing import Dict, Set, List, Tuple
from typing import Dict, Set, List, Tuple
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import csv
import os



# def _get_documents_related_to_query(weighted_inverted_index: Dict[str, list], weighted_query_terms: dict) -> Set[str]:
    # """
    # Retrieve only the documents that contain all terms present in the query.

    # Args:
    #     weighted_inverted_index (Dict[str, list]): weighted inverted index of documents in corpus.
    #     weighted_query_terms (dict): dictionary of weighted query terms.

    # Returns:
    #     A set of documents that are relevant to the query.
    # """
    # # استخراج مفاتيح (الكلمات) الفهرس ومفاتيح الاستعلام
    # inverted_index_keys = set(weighted_inverted_index.keys())
    # query_keys = set(weighted_query_terms.keys())

    # # إيجاد الكلمات المشتركة بين الفهرس والاستعلام
    # shared_items = inverted_index_keys & query_keys
    # print("Shared items:", shared_items)

    # if not shared_items:
    #     return set()

    # # إنشاء مجموعة لحفظ المستندات المشتركة
    # documents = None

    # for item in shared_items:
    #     # جلب جميع المستندات التي تحتوي على الكلمة المشتركة
    #     item_docs = set(doc_key for docs in weighted_inverted_index[item] for doc_key in docs.keys())

    #     if documents is None:
    #         # أول مجموعة من المستندات المشتركة
    #         documents = item_docs
    #     else:
    #         # الاحتفاظ فقط بالمستندات المشتركة بين جميع الكلمات المشتركة
    #         documents &= item_docs

    #     # إذا أصبحت مجموعة المستندات فارغة، يمكن التوقف
    #     if not documents:
    #         break
    # return documents

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from inverted_index import get_document_vector, get_weighted_inverted_index
from query_processing import calculate_query_tfidf


# def _get_documents_related_to_query(weighted_inverted_index: Dict[str, list], weighted_query_terms: dict) -> Set[str]:
#     """
#          retrieve only the documents that contain terms present in the query.

#         Args:
#             weighted_inverted_index (Dict[str, list]): weighted inverted index of documents in corpus.
#             weighted_query (dict): dictionary of weighted query terms.

#         Returns:
#             A set of documents that are relevant to the query
#     """
#     # both weighted_inverted_index and weighted_query_terms must be sorted ...
#     documents = set()
#     inverted_index_keys = list(weighted_inverted_index.keys())
    
#     query_keys = list(weighted_query_terms.keys())
    
#     shared_items = [x for x in inverted_index_keys if x in query_keys]
    
#     for item in shared_items:
#         for docs in weighted_inverted_index[item]:
#             for doc_key in docs:
#                 documents.add(doc_key)
#     print(documents)
#     return documents

def _get_documents_related_to_query(weighted_inverted_index: Dict[str, list], weighted_query_terms: dict) -> Set[str]:
    """
    Retrieve only the documents that contain terms present in the query.

    Args:
        weighted_inverted_index (Dict[str, list]): weighted inverted index of documents in corpus.
        weighted_query (dict): dictionary of weighted query terms.

    Returns:
        A set of documents that are relevant to the query
    """
    documents = set()
    inverted_index_keys = list(weighted_inverted_index.keys())
    query_keys = list(weighted_query_terms.keys())

    # print("Inverted index keys:", inverted_index_keys)
    # print("Query keys:", query_keys)

    shared_items = [x for x in inverted_index_keys if x in query_keys]
    print("Shared items:", shared_items)

    document_count = 0
    for item in shared_items:
        # print(f"Processing term: {item}")
        for docs in weighted_inverted_index[item]:
            # print(f"Docs for term {item}: {docs}")
            for doc_key in docs:
                # print(f"Adding document {doc_key} for term {item}")
                document_count += 1
                documents.add(doc_key)
    
    
    return documents


def _get_document_vectors(documents: Set[str], dataset_name: str) -> Dict[str, Dict[str, float]]:
    """
    Get the TF-IDF vector for a specified documents in a given dataset.

    Args:
        dataset_name (str): The name of the dataset to use. Can be either "technology" or "quora".
        documents set[str]: documents to get the vector for.

    Returns:
        A dictionary representing the TF-IDF vector for the documents. the keys are document ids and the values are
         dictionaries their keys are terms and the values are the TF-IDF values for each term.
    """
    document_vectors = {}
    for doc_id in documents:
        document_vectors[doc_id] = get_document_vector(dataset_name, doc_id)
    return document_vectors


def _get_matrix_from_documents_and_query_vectors(document_vectors: Dict[str, Dict[str, float]],
                                                 query_vector: Dict[str, float]) \
        -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
        Convert document_vectors and query_vector into a matrix.

        Args:
            document_vectors (dict[str, dict[str, float]]): A dictionary the keys are doc_ids and the values are
            dictionaries representing documents. Each dictionary has terms as keys and weights as values.
            query_vector (Dict[str, float]): A dictionary the keys are terms and the values are weights

        Returns:
            1) A matrix where each row corresponds to a document and each column corresponds to a unique term in the
            documents. The value in each cell represents the weight of a term in a document.
            2) A matrix where of one row corresponds to the query and each column corresponds to a unique term in the
            query. The value in each cell represents the weight of a term in the query.
            3) a list of doc_ids to map between rows in matrix and doc_ids
    """
    doc_ids = list(document_vectors.keys())
    doc_list = list(document_vectors.values())
    vectorizer = DictVectorizer()
    docs_terms_matrix = vectorizer.fit_transform(doc_list)
    query_matrix = vectorizer.transform(query_vector)
    return docs_terms_matrix, query_matrix, doc_ids


def ranking(query: str, dataset: str) -> Dict[str, float]:
    """
    ranking the documents by calculate the cosine similarity between a query and the documents in the docs_terms_matrix

    Args:
        query (str): the query to calculate cosine similarity for with documents
        dataset (str): The name of the dataset to use. Can be either "technology" or "quora".

    Returns:
        Dict the keys is the docs_id and the values are the similarity sorted in descending order
    """
    # first function
    weighted_inverted_index = get_weighted_inverted_index(dataset)
    query_vector = calculate_query_tfidf(query, dataset)
    related_documents = _get_documents_related_to_query(weighted_inverted_index, query_vector)
    # second function
    document_vectors = _get_document_vectors(related_documents, dataset)

    # third function
    try:
        matrix, query_matrix, doc_ids = _get_matrix_from_documents_and_query_vectors(document_vectors, query_vector)
        similarity = cosine_similarity(query_matrix, matrix)
        document_ranking = dict(zip(doc_ids, similarity.flatten()))
        sorted_dict = dict(sorted(document_ranking.items(), key=lambda item: item[1], reverse=True))
        return sorted_dict
    except ValueError:
        return {}


# # ['912104_2', '2849096_5', '2849096_3', '1225007_2', '684385_12', '1061393_11', '2854712_4', '264820_28', '150871_1', '2883540_9', '3228330_2', '172962_6', '2764410_7',
# #  '1939398_19', '3842053_19', '2400167_1', '149933_0', '2804023_2', '1390248_2', '2852598_4']

# # ['912104_2', '2849096_5', '2849096_3', '1225007_2', '684385_12', '1061393_11', '2854712_4', '264820_28', '150871_1', '2883540_9', '3228330_2', '172962_6', '2764410_7', 
# # '1939398_19', '3842053_19', '2400167_1', '149933_0', '2804023_2', '1390248_2', '2852598_4']

# # ['3572358_12', '3751940_3', '4396465_12', '175971_3', '4085899_6', '4185324_1', '11706_8', 
# # '250849_3', '2332549_8', '3248251_12', '2288540_4', '1205004_2']
# import numpy as np
# from sklearn.feature_extraction import DictVectorizer
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from typing import Dict, List, Set, Tuple

# from inverted_index import get_document_vector, get_weighted_inverted_index
# from query_processing import calculate_query_tfidf


# def _get_documents_related_to_query(weighted_inverted_index: Dict[str, list], weighted_query_terms: dict) -> Set[str]:
#     """
#     Retrieve only the documents that contain terms present in the query.

#     Args:
#         weighted_inverted_index (Dict[str, list]): weighted inverted index of documents in corpus.
#         weighted_query (dict): dictionary of weighted query terms.

#     Returns:
#         A set of documents that are relevant to the query.
#     """
#     documents = set()
#     inverted_index_keys = list(weighted_inverted_index.keys())
#     query_keys = list(weighted_query_terms.keys())
#     shared_items = [x for x in inverted_index_keys if x in query_keys]
#     print("Shared items:", shared_items)

#     for item in shared_items:
#         for docs in weighted_inverted_index[item]:
#             for doc_key in docs:
#                 documents.add(doc_key)
#     return documents


# def _get_document_vectors(documents: Set[str], dataset_name: str) -> Dict[str, Dict[str, float]]:
#     """
#     Get the TF-IDF vector for specified documents in a given dataset.

#     Args:
#         dataset_name (str): The name of the dataset to use.
#         documents (set[str]): documents to get the vector for.

#     Returns:
#         A dictionary representing the TF-IDF vector for the documents. The keys are document ids and the values are
#         dictionaries their keys are terms and the values are the TF-IDF values for each term.
#     """
#     document_vectors = {}
#     for doc_id in documents:
#         document_vectors[doc_id] = get_document_vector(dataset_name, doc_id)
#     return document_vectors


# def _get_matrix_from_documents_and_query_vectors(document_vectors: Dict[str, Dict[str, float]],
#                                                  query_vector: Dict[str, float]) \
#         -> Tuple[np.ndarray, np.ndarray, List[str]]:
#     """
#     Convert document_vectors and query_vector into a matrix.

#     Args:
#         document_vectors (dict[str, dict[str, float]]): A dictionary where the keys are doc_ids and the values are
#         dictionaries representing documents. Each dictionary has terms as keys and weights as values.
#         query_vector (Dict[str, float]): A dictionary where the keys are terms and the values are weights.

#     Returns:
#         1) A matrix where each row corresponds to a document and each column corresponds to a unique term in the
#         documents. The value in each cell represents the weight of a term in a document.
#         2) A matrix where one row corresponds to the query and each column corresponds to a unique term in the
#         query. The value in each cell represents the weight of a term in the query.
#         3) a list of doc_ids to map between rows in matrix and doc_ids.
#     """
#     doc_ids = list(document_vectors.keys())
#     doc_list = list(document_vectors.values())
#     vectorizer = DictVectorizer()
#     docs_terms_matrix = vectorizer.fit_transform(doc_list)
#     query_matrix = vectorizer.transform([query_vector])
#     return docs_terms_matrix, query_matrix, doc_ids


# def ranking(query: str, dataset: str) -> Dict[str, float]:
#     """
#     Rank the documents by calculating the cosine similarity between a query and the documents in the docs_terms_matrix.

#     Args:
#         query (str): the query to calculate cosine similarity for with documents.
#         dataset (str): The name of the dataset to use.

#     Returns:
#         A dictionary where the keys are doc_ids and the values are the similarity scores, sorted in descending order.
#     """
#     weighted_inverted_index = get_weighted_inverted_index(dataset)
#     query_vector = calculate_query_tfidf(query, dataset)
#     related_documents = _get_documents_related_to_query(weighted_inverted_index, query_vector)
#     document_vectors = _get_document_vectors(related_documents, dataset)

#     try:
#         matrix, query_matrix, doc_ids = _get_matrix_from_documents_and_query_vectors(document_vectors, query_vector)
#         similarity = cosine_similarity(query_matrix, matrix)
#         document_ranking = dict(zip(doc_ids, similarity.flatten()))
#         sorted_dict = dict(sorted(document_ranking.items(), key=lambda item: item[1], reverse=True))
#         return sorted_dict
#     except ValueError:
#         return {}
