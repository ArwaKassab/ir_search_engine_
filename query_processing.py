import math
import shelve
from collections import defaultdict
from typing import Dict
import pandas as pd

import ir_datasets

# from process_data import get_preprocessed_text,get_preprocessed_tokens_terms
from text_preprocessing import get_preprocessed_text_terms

def __get_queries_corpus(dataset_name: str) -> Dict[str, str]:
    """
    Get a corpus of queries for a given dataset name.

    Args:
        dataset_name: The name of the dataset to use. Can be either "technology" or "quora".

    Returns:
        A dictionary mapping query IDs to query content.
    """
    if dataset_name == "antique":

        file_path = "C:\\Users\\ARWAA\\.ir_datasets\\antique\\processed_queries.tsv"
        # file_path = "C:\\Users\\ARWAA\\Desktop\\IR3\\antique-test-queries.tsv"
        df = pd.read_csv(file_path, sep='\t', header=None, names=['query_id', 'query_content'])
        queries_corpus = dict(zip(df['query_id'], df['query_content']))
        return queries_corpus
    
    if dataset_name == "wiki":
        file_path = "C:\\Users\\ARWAA\\Desktop\\IR3\\wiki\\cleaned_queries.tsv"
        df = pd.read_csv(file_path, sep='\t', header=None, names=['query_id', 'query_content'])
        queries_corpus = dict(zip(df['query_id'], df['query_content']))
        return queries_corpus

    return queries_corpus

    


# def _get_preprocessed_text_terms(text: str, dataset_name: str):
#     tokens = get_preprocessed_text(text)
#     tokens = get_preprocessed_tokens_terms(tokens)
#     print("تم _get_preprocessed_text_terms")
#     return tokens

def _get_preprocessed_text_terms(text: str, dataset_name: str):
    tokens = get_preprocessed_text_terms(text,dataset_name)
    print("تم _get_preprocessed_text_terms")
    return tokens



def create_unweighted_inverted_index(dataset_name) -> None:
    corpus = __get_queries_corpus(dataset_name)
    inverted_index = defaultdict(list)
    for query_id, query_content in corpus.items():
        print(query_id)
        terms = _get_preprocessed_text_terms(query_content, dataset_name)
        unique_terms = set(terms)
        for term in unique_terms:
            inverted_index[term].append(query_id)
    # storing inverted index in shelve
    # Open a "shelve" file to store the inverted index
    with shelve.open('db/' + dataset_name + '_queries_inverted_index.db') as db:
        # Store the inverted index in the "shelve" file
        db['inverted_index'] = inverted_index


def _get_unweighted_inverted_index(dataset_name) -> Dict[str, list]:
    # Inverted index
    with shelve.open('db/' + dataset_name + '_queries_inverted_index.db') as db:
        queries_inverted_index = db['inverted_index']
    return queries_inverted_index


def _calculate_tf(query: str, dataset_name: str) -> Dict[str, float]:
    """
    Calculate the term frequency (TF) for a given query.

    Args:
        query: The query to calculate the TF for.
        dataset_name:The name of the dataset

    Returns:
        A dictionary representing the TF for the given query. The keys are terms and the values are the TF values for
         each term.
    """
    tf = {}
    terms = _get_preprocessed_text_terms(query, dataset_name)
    term_count = len(terms)
    for term in terms:
        tf[term] = terms.count(term) / term_count
    return tf


def _calculate_idf(corpus: Dict[str, str], unweighted_inverted_index: Dict[str, list]) -> Dict[str, float]:
    """
    Calculate the inverse document frequency (IDF) for a given corpus and unweighted inverted index.

    Args:
        corpus: A dictionary mapping query IDs to query content.
        unweighted_inverted_index: An unweighted inverted index for the given corpus.

    Returns:
        A dictionary representing the IDF for the given corpus. The keys are terms and the values are the IDF values for
         each term.
    """
    idf = {}
    n_queries = len(corpus)
    # inverted_index = create_inverted_index(corpus)
    for term, query_ids in unweighted_inverted_index.items():
        idf[term] = math.log10(n_queries / len(query_ids))
    return idf


def calculate_query_tfidf(query: str, dataset_name: str) -> Dict[
    str, float]:
    """
    Calculate the TF-IDF for a given query and dataset name.

    Args:
        query: The query to calculate the TF-IDF for.
        dataset_name:The name of the dataset

    Returns:
        A dictionary representing the TF-IDF for the given query. The keys are terms and the values are the TF-IDF
        values for each term.
    """
    tfidf = {}
    tf = _calculate_tf(query, dataset_name)
    corpus = __get_queries_corpus(dataset_name)
    unweighted_inverted_index = _get_unweighted_inverted_index(dataset_name)
    idf = _calculate_idf(corpus, unweighted_inverted_index)
    for term in tf:
        tfidf[term] = tf[term] * idf.get(term, math.log10(
            len(corpus) / 1))  # we need a default value of idf in case of a new term in query(high idf)
    
    return tfidf


__all__ = ['calculate_query_tfidf', 'create_unweighted_inverted_index']


# import math
# import shelve
# from collections import defaultdict
# from typing import Dict
# import pandas as pd

# import ir_datasets
# from text_preprocessing import get_preprocessed_text_terms
# from sklearn.feature_extraction.text import TfidfVectorizer

# def __get_queries_corpus(dataset_name: str) -> Dict[str, str]:
#     """
#     Get a corpus of queries for a given dataset name.

#     Args:
#         dataset_name: The name of the dataset to use.

#     Returns:
#         A dictionary mapping query IDs to query content.
#     """
#     if dataset_name == "antique":
#         file_path = "C:\\Users\\ARWAA\\.ir_datasets\\antique\\processed_queries.tsv"
#         df = pd.read_csv(file_path, sep='\t', header=None, names=['query_id', 'query_content'])
#         queries_corpus = dict(zip(df['query_id'], df['query_content']))
#         return queries_corpus
    
#     if dataset_name == "wiki":
#         file_path = "C:\\Users\\ARWAA\\Desktop\\IR3\\wiki\\queries.tsv"
#         df = pd.read_csv(file_path, sep='\t', header=None, names=['query_id', 'query_content'])
#         queries_corpus = dict(zip(df['query_id'], df['query_content']))
#         return queries_corpus

#     return {}

# def _get_preprocessed_text_terms(text: str, dataset_name: str):
#     tokens = get_preprocessed_text_terms(text, dataset_name)
#     print("تم _get_preprocessed_text_terms")
#     return tokens

# def create_unweighted_inverted_index(dataset_name) -> None:
#     corpus = __get_queries_corpus(dataset_name)
#     inverted_index = defaultdict(list)
#     for query_id, query_content in corpus.items():
#         print(query_id)
#         terms = _get_preprocessed_text_terms(query_content, dataset_name)
#         unique_terms = set(terms)
#         for term in unique_terms:
#             inverted_index[term].append(query_id)
#     # storing inverted index in shelve
#     with shelve.open('db/' + dataset_name + '_queries_inverted_index.db') as db:
#         db['inverted_index'] = inverted_index

# def _get_unweighted_inverted_index(dataset_name) -> Dict[str, list]:
#     with shelve.open('db/' + dataset_name + '_queries_inverted_index.db') as db:
#         queries_inverted_index = db['inverted_index']
#     return queries_inverted_index

# def calculate_query_tfidf(query: str, dataset_name: str) -> Dict[str, float]:
#     """
#     Calculate the TF-IDF for a given query and dataset name.

#     Args:
#         query: The query to calculate the TF-IDF for.
#         dataset_name: The name of the dataset.

#     Returns:
#         A dictionary representing the TF-IDF for the given query. The keys are terms and the values are the TF-IDF
#         values for each term.
#     """
#     corpus = __get_queries_corpus(dataset_name) 
#     unweighted_inverted_index = _get_unweighted_inverted_index(dataset_name)
#     corpus = {term: ' '.join([str(doc) for doc in docs]) for term, docs in unweighted_inverted_index.items()}
#     processed_query = ' '.join(_get_preprocessed_text_terms(query, dataset_name))
#     print('Processed query:', processed_query)
    
#     # استخدام TfidfVectorizer لحساب مصفوفة TF-IDF
#     vectorizer = TfidfVectorizer(max_df=0.95, min_df=0.001, ngram_range=(1, 2), max_features=10000)
#     tfidf_matrix = vectorizer.fit_transform(list(corpus.values()) + [processed_query])
    
#     terms = vectorizer.get_feature_names_out()
#     query_vector = tfidf_matrix[-1].toarray().flatten()
    
#     tfidf = {terms[i]: query_vector[i] for i in range(len(terms)) if query_vector[i] > 0}
    
#     # طباعة المصطلحات المقسمة والـ TF-IDF
#     print("Terms:", terms)
#     print("Query TF-IDF Vector:", query_vector)
    
#     return tfidf
#     # def calculate_query_tfidf(query: str, dataset_name: str) -> Dict[
# #     str, float]:
# #     """
# #     Calculate the TF-IDF for a given query and dataset name.

# #     Args:
# #         query: The query to calculate the TF-IDF for.
# #         dataset_name:The name of the dataset

# #     Returns:
# #         A dictionary representing the TF-IDF for the given query. The keys are terms and the values are the TF-IDF
# #         values for each term.
# #     """
# #     tfidf = {}
# #     tf = _calculate_tf(query, dataset_name)
# #     corpus = __get_queries_corpus(dataset_name)
# #     unweighted_inverted_index = _get_unweighted_inverted_index(dataset_name)
# #     idf = _calculate_idf(corpus, unweighted_inverted_index)
# #     for term in tf:
# #         tfidf[term] = tf[term] * idf.get(term, math.log10(
# #             len(corpus) / 1))  # we need a default value of idf in case of a new term in query(high idf)
    
# #     return tfidf

# __all__ = ['calculate_query_tfidf', 'create_unweighted_inverted_index']
