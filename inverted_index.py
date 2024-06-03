
import math
import shelve
from collections import defaultdict
from typing import Dict
import pandas as pd

import ir_datasets

# from process_data import get_preprocessed_tokens_terms
# from process_data import get_preprocessed_text
from text_preprocessing import get_preprocessed_text_terms
from crawling import expand_document_with_crawled_data

# Assign indexes and vectors to global variables, and initialize them at the runtime using [set_global_variables],
# for reducing database access time
_antique_weighted_inverted_index = None
_antique_documents_vector = None
_wiki_weighted_inverted_index = None
_wiki_documents_vector = None



def set_inverted_index_store_global_variables() -> None:
    """
    Get a weighted inverted index for both technology and quora from a "shelve" file and assign it to its global variable
    Get a documents vector for both technology and quora from a "shelve" file and assign it to its global variable

    Args:
        No args
    Returns:
        None
    """
    global _antique_weighted_inverted_index
    global _antique_documents_vector
    global _wiki_weighted_inverted_index
    global _wiki_documents_vector

    # Inverted index
    with shelve.open('db/' + "antique" + '_inverted_index.db') as db:
        if 'inverted_index' in db:
            _antique_weighted_inverted_index = db['inverted_index']
        else:
            print("Error: 'inverted_index' key not found in the shelve database.")

    # Document Vector
    with shelve.open('db/' + "antique" + '_documents_vector.db') as db:
        if 'documents_vector' in db:
            _antique_documents_vector = db["documents_vector"]
        else:
            print("Error: 'documents_vector' key not found in the shelve database.")
    
    with shelve.open('db/' + "wiki" + '_inverted_index.db') as db:
        if 'inverted_index' in db:
            _wiki_weighted_inverted_index = db['inverted_index']
        else:
            print("Error: 'inverted_index' key not found in the shelve database.")

    # Document Vector
    with shelve.open('db/' + "wiki" + '_documents_vector.db') as db:
        if 'documents_vector' in db:
            _wiki_documents_vector = db["documents_vector"]
        else:
            print("Error: 'documents_vector' key not found in the shelve database.")
    



def store_weighted_inverted_index(dataset_name: str, weighted_inverted_index: Dict) -> None:
    with shelve.open('db/' + dataset_name + '_inverted_index.db') as db:
        db['inverted_index'] = weighted_inverted_index

# # التابع لإنشاء معكوس موزون للوثائق
def create_weighted_inverted_index_from_tsv(corpus: Dict[str, str], dataset_name: str) -> None:
       
    weighted_inverted_index = defaultdict(list)
    vectors = _create_docs_vectors(corpus, dataset_name)
    for doc_id, doc_weighted_terms in vectors.items():
        for term, weight in doc_weighted_terms.items():
            weighted_inverted_index[term].append({doc_id: weight})
    
    store_weighted_inverted_index(dataset_name, weighted_inverted_index)
    
def create_crawled_content_index_from_tsv(corpus: Dict[str, str], dataset_name: str) -> None:
    """
    Create a weighted inverted index from a given corpus, including only content from crawled URLs within documents.
    
    Args:
        corpus: A dictionary mapping document IDs to document content.
        dataset_name: The name of the dataset to use.
        
    Returns:
        None
    """
    weighted_inverted_index = defaultdict(list)
    crawled_content_corpus = {}

    # Process each document to include only crawled content
    for doc_id, doc_content in corpus.items():
        crawled_content = expand_document_with_crawled_data(doc_content)
        if crawled_content:
            crawled_content_corpus[doc_id] = crawled_content

    # Create new weighted inverted index from crawled content
    vectors = _create_docs_vectors(crawled_content_corpus, dataset_name)
    for doc_id, doc_weighted_terms in vectors.items():
        for term, weight in doc_weighted_terms.items():
            weighted_inverted_index[term].append({doc_id: weight})

    # Store the new weighted inverted index without merging
    store_weighted_inverted_index(dataset_name + '_crawled', weighted_inverted_index)



def _create_docs_vectors(corpus: Dict[str, str], dataset_name: str) -> Dict[str, Dict[str, float]]:
    """
    Create a dictionary of TF-IDF vectors for each document in the corpus.

    Args:
        corpus: A dictionary mapping document IDs to document content.
        dataset_name: The name of the dataset to use. Can be either "technology" or "quora".

    Returns:
        A dictionary where the keys are document IDs and the values are dictionaries representing the TF-IDF vector for
        each document. The keys of the inner dictionaries are terms and the values are the TF-IDF weights for each term.
    """
    unweighted_inverted_index = _create_unweighted_inverted_index(corpus, dataset_name)
    vectors = {}
    for doc_id, doc_content in corpus.items():
        vectors[doc_id] = _calculate_tfidf(doc_content, corpus, unweighted_inverted_index, dataset_name)
    with shelve.open('db/' + dataset_name + '_documents_vector.db') as db:
        db["documents_vector"] = vectors
    print("تم documents_vector")

    return vectors


def _create_unweighted_inverted_index(corpus: Dict[str, str], dataset_name: str) -> Dict[str, list]:
    """
    Create an unweighted inverted index from a corpus of documents.

    Args:
        corpus: A dictionary mapping document IDs to document content.
    Returns:
        A dictionary representing the unweighted inverted index. The keys are terms and the values are lists of document
         IDs containing the term.
    """
    inverted_index = defaultdict(list)
    for doc_id, doc_content in corpus.items():
        terms = _get_preprocessed_text_terms(doc_content, dataset_name)
        unique_terms = set(terms)
        for term in unique_terms:
            inverted_index[term].append(doc_id)
    print("تم _create_unweighted_inverted_index-")
    return dict(inverted_index)


# def _get_preprocessed_text_terms(text: str, dataset_name: str):
#     tokens = get_preprocessed_text(text)
#     tokens = get_preprocessed_tokens_terms(tokens)
#     print("تم _get_preprocessed_text_terms")
#     return tokens
def _get_preprocessed_text_terms(text: str, dataset_name: str):
    tokens = get_preprocessed_text_terms(text,dataset_name)
    print("تم _get_preprocessed_text_terms")
    return tokens




def _calculate_tfidf(document: str, corpus: Dict[str, str], unweighted_inverted_index: Dict[str, list],
                     dataset_name: str) -> Dict[str, float]:
    """
    Calculate the TF-IDF for a given document and corpus.

    Args:
        document: The document to calculate the TF-IDF for.
        corpus: A dictionary mapping document IDs to document content.
        unweighted_inverted_index: An unweighted inverted index for the given corpus.
        dataset_name: The name of the dataset to use. Can be either "technology" or "quora".

    Returns:
        A dictionary representing the TF-IDF for the given document. The keys are terms and the values are the TF-IDF
        values for each term.
    """
    tfidf = {}
    tf = _calculate_tf(document, dataset_name)
    idf = _calculate_idf(corpus, unweighted_inverted_index)
    for term in tf:
        tfidf[term] = tf[term] * idf[term]
    print("تم tfidf")
    return tfidf


def _calculate_tf(document: str, dataset_name: str) -> Dict[str, float]:
    """
    Calculate the term frequency (TF) for a given document.

    Args:
        document: The document to calculate the TF for.
        dataset_name: The name of the dataset to use. Can be either "technology" or "quora".

    Returns:
        A dictionary representing the TF for the given document. The keys are terms and the values are the TF values for
         each term.
    """
    tf = {}
    terms = _get_preprocessed_text_terms(document, dataset_name)
    term_count = len(terms)
    for term in terms:
        tf[term] = terms.count(term) / term_count
    print("تم tf")
    return tf


def _calculate_idf(corpus: Dict[str, str], unweighted_inverted_index: Dict[str, list]) -> Dict[str, float]:
    """
    Calculate the inverse document frequency (IDF) for a given corpus and unweighted inverted index.

    Args:
        corpus: A dictionary mapping document IDs to document content.
        unweighted_inverted_index: An unweighted inverted index for the given corpus.

    Returns:
        A dictionary representing the IDF for the given corpus. The keys are terms and the values are the IDF values for
         each term.
    """
    idf = {}
    n_docs = len(corpus)
    for term, doc_ids in unweighted_inverted_index.items():
        idf[term] = math.log10(n_docs / len(doc_ids))
    print("تم idf")
    return idf


def get_weighted_inverted_index(dataset_name: str) -> Dict[str, list]:
    """
    Get a weighted inverted index from a "shelve" file.

    Args:
        dataset_name: The name of the dataset to use. Can be either "technology" or "quora".

    Returns:
        A dictionary representing the weighted inverted index. The keys are terms and the values are lists of
        dictionaries representing the documents containing the term. The keys of the inner dictionaries are document IDs
        and the values are the TF-IDF weights for each term in each document.
    Examples of use:
        index=get_weighted_inverted_index("technology")
        print(index["You"])
    """
    return globals()["_" + dataset_name + "_weighted_inverted_index"]


def get_document_vector(dataset_name: str, doc_id: str) -> Dict[str, float]:
    """
    Get the TF-IDF vector for a specified document in a given dataset.

    Args:
        dataset_name (str): The name of the dataset to use. Can be either "technology" or "quora".
        doc_id (str): The ID of the document to get the vector for.
        
    Returns:
        A dictionary representing the TF-IDF vector for the specified document. The keys are terms and the values are
        the TF-IDF values for each term.
    """
    return globals()["_" + dataset_name + "_documents_vector"][doc_id]


def get_documents_vector(dataset_name: str) -> Dict[str, Dict[str, float]]:
    """
    Get the TF-IDF vector for a documents in a given dataset.

    Args:
        dataset_name (str): The name of the dataset to use. Can be either "technology" or "quora".

    Returns:
        A dictionary representing the TF-IDF vector for documents. The keys are document ids and the values are lists of
        dictionaries representing the terms in the document. The keys of the inner dictionaries are terms
        and the values are the TF-IDF weights for each term in each document.
    """
    return globals()["_" + dataset_name + "_documents_vector"]


__all__ = ['create_weighted_inverted_index_from_tsv','create_crawled_content_index_from_tsv', 'get_weighted_inverted_index', 'get_document_vector',
           'set_inverted_index_store_global_variables', 'get_documents_vector']


# import math
# import shelve
# from collections import defaultdict
# from typing import Dict
# import pandas as pd

# import ir_datasets
# from text_preprocessing import get_preprocessed_text_terms
# from crawling import expand_document_with_crawled_data
# from sklearn.feature_extraction.text import TfidfVectorizer

# # Assign indexes and vectors to global variables, and initialize them at the runtime using [set_global_variables],
# # for reducing database access time
# _antique_weighted_inverted_index = None
# _antique_documents_vector = None
# _wiki_weighted_inverted_index = None
# _wiki_documents_vector = None

# def set_inverted_index_store_global_variables() -> None:
#     """
#     Get a weighted inverted index for both technology and quora from a "shelve" file and assign it to its global variable
#     Get a documents vector for both technology and quora from a "shelve" file and assign it to its global variable

#     Args:
#         No args
#     Returns:
#         None
#     """
#     global _antique_weighted_inverted_index
#     global _antique_documents_vector
#     global _wiki_weighted_inverted_index
#     global _wiki_documents_vector

#     # Inverted index
#     with shelve.open('db/' + "antique" + '_inverted_index.db') as db:
#         if 'inverted_index' in db:
#             _antique_weighted_inverted_index = db['inverted_index']
#         else:
#             print("Error: 'inverted_index' key not found in the shelve database.")

#     # Document Vector
#     with shelve.open('db/' + "antique" + '_documents_vector.db') as db:
#         if 'documents_vector' in db:
#             _antique_documents_vector = db["documents_vector"]
#         else:
#             print("Error: 'documents_vector' key not found in the shelve database.")
    
#     with shelve.open('db/' + "wiki" + '_inverted_index.db') as db:
#         if 'inverted_index' in db:
#             _wiki_weighted_inverted_index = db['inverted_index']
#         else:
#             print("Error: 'inverted_index' key not found in the shelve database.")

#     # Document Vector
#     with shelve.open('db/' + "wiki" + '_documents_vector.db') as db:
#         if 'documents_vector' in db:
#             _wiki_documents_vector = db["documents_vector"]
#         else:
#             print("Error: 'documents_vector' key not found in the shelve database.")
    
# def store_weighted_inverted_index(dataset_name: str, weighted_inverted_index: Dict) -> None:
#     with shelve.open('db/' + dataset_name + '_inverted_index.db') as db:
#         db['inverted_index'] = weighted_inverted_index

# # التابع لإنشاء معكوس موزون للوثائق
# def create_weighted_inverted_index_from_tsv(corpus: Dict[str, str], dataset_name: str) -> None:
#     weighted_inverted_index = defaultdict(list)
#     vectors = _create_docs_vectors(corpus, dataset_name)
#     for doc_id, doc_weighted_terms in vectors.items():
#         for term, weight in doc_weighted_terms.items():
#             weighted_inverted_index[term].append({doc_id: weight})
    
#     store_weighted_inverted_index(dataset_name, weighted_inverted_index)
    
# def create_crawled_content_index_from_tsv(corpus: Dict[str, str], dataset_name: str) -> None:
#     """
#     Create a weighted inverted index from a given corpus, including only content from crawled URLs within documents.
    
#     Args:
#         corpus: A dictionary mapping document IDs to document content.
#         dataset_name: The name of the dataset to use.
        
#     Returns:
#         None
#     """
#     weighted_inverted_index = defaultdict(list)
#     crawled_content_corpus = {}

#     # Process each document to include only crawled content
#     for doc_id, doc_content in corpus.items():
#         crawled_content = expand_document_with_crawled_data(doc_content)
#         if crawled_content:
#             crawled_content_corpus[doc_id] = crawled_content

#     # Create new weighted inverted index from crawled content
#     vectors = _create_docs_vectors(crawled_content_corpus, dataset_name)
#     for doc_id, doc_weighted_terms in vectors.items():
#         for term, weight in doc_weighted_terms.items():
#             weighted_inverted_index[term].append({doc_id: weight})

#     # Store the new weighted inverted index without merging
#     store_weighted_inverted_index(dataset_name + '_crawled', weighted_inverted_index)

# def _create_docs_vectors(corpus: Dict[str, str], dataset_name: str) -> Dict[str, Dict[str, float]]:
#     """
#     Create a dictionary of TF-IDF vectors for each document in the corpus.

#     Args:
#         corpus: A dictionary mapping document IDs to document content.
#         dataset_name: The name of the dataset to use.

#     Returns:
#         A dictionary where the keys are document IDs and the values are dictionaries representing the TF-IDF vector for
#         each document. The keys of the inner dictionaries are terms and the values are the TF-IDF weights for each term.
#     """
#     processed_corpus = {doc_id: ' '.join(get_preprocessed_text_terms(doc_content, dataset_name)) for doc_id, doc_content in corpus.items()}
    
#     # استخدام TfidfVectorizer لحساب مصفوفة TF-IDF
#     vectorizer = TfidfVectorizer(max_df=0.85, min_df=0.01, stop_words='english', ngram_range=(1, 2), max_features=1000)
#     tfidf_matrix = vectorizer.fit_transform(processed_corpus.values())
#     terms = vectorizer.get_feature_names_out()

#     vectors = {}
#     for idx, doc_id in enumerate(processed_corpus.keys()):
#         vectors[doc_id] = {term: tfidf_matrix[idx, i] for i, term in enumerate(terms) if tfidf_matrix[idx, i] > 0}
    
#     with shelve.open('db/' + dataset_name + '_documents_vector.db') as db:
#         db["documents_vector"] = vectors
#     print("تم documents_vector")

#     return vectors

# def _create_unweighted_inverted_index(corpus: Dict[str, str], dataset_name: str) -> Dict[str, list]:
#     """
#     Create an unweighted inverted index from a corpus of documents.

#     Args:
#         corpus: A dictionary mapping document IDs to document content.
#     Returns:
#         A dictionary representing the unweighted inverted index. The keys are terms and the values are lists of document
#          IDs containing the term.
#     """
#     inverted_index = defaultdict(list)
#     for doc_id, doc_content in corpus.items():
#         terms = get_preprocessed_text_terms(doc_content, dataset_name)
#         unique_terms = set(terms)
#         for term in unique_terms:
#             inverted_index[term].append(doc_id)
#     print("تم _create_unweighted_inverted_index-")
#     return dict(inverted_index)

# def get_weighted_inverted_index(dataset_name: str) -> Dict[str, list]:
#     """
#     Get a weighted inverted index from a "shelve" file.

#     Args:
#         dataset_name: The name of the dataset to use.

#     Returns:
#         A dictionary representing the weighted inverted index. The keys are terms and the values are lists of
#         dictionaries representing the documents containing the term. The keys of the inner dictionaries are document IDs
#         and the values are the TF-IDF weights for each term in each document.
#     """
#     return globals()["_" + dataset_name + "_weighted_inverted_index"]

# def get_document_vector(dataset_name: str, doc_id: str) -> Dict[str, float]:
#     """
#     Get the TF-IDF vector for a specified document in a given dataset.

#     Args:
#         dataset_name (str): The name of the dataset to use.
#         doc_id (str): The ID of the document to get the vector for.
        
#     Returns:
#         A dictionary representing the TF-IDF vector for the specified document. The keys are terms and the values are
#         the TF-IDF values for each term.
#     """
#     return globals()["_" + dataset_name + "_documents_vector"][doc_id]

# def get_documents_vector(dataset_name: str) -> Dict[str, Dict[str, float]]:
#     """
#     Get the TF-IDF vector for a documents in a given dataset.

#     Args:
#         dataset_name (str): The name of the dataset to use.

#     Returns:
#         A dictionary representing the TF-IDF vector for documents. The keys هي document ids and the values are lists of
#         dictionaries representing the terms in the document. The keys of the inner dictionaries هي terms
#         and the values هي the TF-IDF weights for each term in each document.
#     """
#     return globals()["_" + dataset_name + "_documents_vector"]

# __all__ = ['create_weighted_inverted_index_from_tsv','create_crawled_content_index_from_tsv', 'get_weighted_inverted_index', 'get_document_vector',
#            'set_inverted_index_store_global_variables', 'get_documents_vector']
