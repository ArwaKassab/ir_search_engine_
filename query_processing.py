import math
import shelve
from collections import defaultdict
from typing import Dict
import pandas as pd

import ir_datasets


from text_preprocessing import get_preprocessed_text_terms

def __get_queries_corpus(dataset_name: str) -> Dict[str, str]:
  
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

    with shelve.open('db/' + dataset_name + '_queries_inverted_index.db') as db:

        db['inverted_index'] = inverted_index


def _get_unweighted_inverted_index(dataset_name) -> Dict[str, list]:

    with shelve.open('db/' + dataset_name + '_queries_inverted_index.db') as db:
        queries_inverted_index = db['inverted_index']
    return queries_inverted_index


def _calculate_tf(query: str, dataset_name: str) -> Dict[str, float]:

    tf = {}
    terms = _get_preprocessed_text_terms(query, dataset_name)
    term_count = len(terms)
    for term in terms:
        tf[term] = terms.count(term) / term_count
    return tf


def _calculate_idf(corpus: Dict[str, str], unweighted_inverted_index: Dict[str, list]) -> Dict[str, float]:

    idf = {}
    n_queries = len(corpus)
    # inverted_index = create_inverted_index(corpus)
    for term, query_ids in unweighted_inverted_index.items():
        idf[term] = math.log10(n_queries / len(query_ids))
    return idf


def calculate_query_tfidf(query: str, dataset_name: str) -> Dict[
    str, float]:

    tfidf = {}
    tf = _calculate_tf(query, dataset_name)
    corpus = __get_queries_corpus(dataset_name)
    unweighted_inverted_index = _get_unweighted_inverted_index(dataset_name)
    idf = _calculate_idf(corpus, unweighted_inverted_index)
    for term in tf:
        tfidf[term] = tf[term] * idf.get(term, math.log10(
            len(corpus) / 1)) 
    
    return tfidf


__all__ = ['calculate_query_tfidf', 'create_unweighted_inverted_index']
