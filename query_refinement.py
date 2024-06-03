
import shelve
from collections import Counter
import pandas as pd
from nltk.corpus import words
from spellchecker import SpellChecker
from typing import Dict

_antique_queries = set()
_wiki_queries = set()
_initialized = False  

def __get_queries_corpus1(file_path: str) -> Dict[str, str]:
    queries_df = pd.read_csv(file_path, sep='\t', header=None, names=['query_id', 'query_text'])
    queries_corpus = dict(zip(queries_df['query_id'], queries_df['query_text']))
    return queries_corpus

def initialize_queries_db() -> None:
    with shelve.open('C:\\Users\\ARWAA\\Desktop\\IR3\\db\\' + "antique" + '_queries.db') as db:
        if 'queries' not in db:
            db['queries'] = set()
    
    with shelve.open('C:\\Users\\ARWAA\\Desktop\\IR3\\db\\' + "wiki" + '_queries.db') as db:
        if 'queries' not in db:
            db['queries'] = set()

def index_query(query: str, dataset_name: str) -> None:
    global _antique_queries
    global _wiki_queries

    if dataset_name == 'antique':
        _antique_queries.add(query)
    else:
        _wiki_queries.add(query)

    with shelve.open('C:\\Users\\ARWAA\\Desktop\\IR3\\db\\' + dataset_name + '_queries.db') as db:
        queries = db['queries']
        queries.add(query)
        db['queries'] = queries

def set_query_refinement_global_variables() -> None:
    global _antique_queries
    global _wiki_queries
    global _initialized

    if _initialized:
        return 

    _antique_queries = set()
    _wiki_queries = set()

    file_path1 = "C:\\Users\\ARWAA\\.ir_datasets\\antique\\processed_queries.tsv"
    file_path2 = "C:\\Users\\ARWAA\\Desktop\\IR3\\wiki\\cleaned_queries.tsv"


    with shelve.open('C:\\Users\\ARWAA\\Desktop\\IR3\\db\\' + "antique" + '_queries.db') as db:
        if 'queries' in db and len(db['queries']) > 0:
            _antique_queries = db['queries']
        else:
            antique_queries = __get_queries_corpus1(file_path1)
            for query_id, query_text in antique_queries.items():
                index_query(query_text, 'antique')
            _antique_queries = set(antique_queries.values())

    with shelve.open('C:\\Users\\ARWAA\\Desktop\\IR3\\db\\' + "wiki" + '_queries.db') as db:
        if 'queries' in db and len(db['queries']) > 0:
            _wiki_queries = db['queries']
        else:
            wiki_queries = __get_queries_corpus1(file_path2)
            for query_id, query_text in wiki_queries.items():
                index_query(query_text, 'wiki')
            _wiki_queries = set(wiki_queries.values())

    _initialized = True 

def _get_query_suggestions(query: str, dataset_name: str) -> list:
    global _antique_queries
    global _wiki_queries

    if dataset_name == 'antique':
        queries = _antique_queries
    else:
        queries = _wiki_queries

    suggestions = []
    query_terms = query.lower().split()
    query_freq = Counter(query_terms)

    for suggest_query in queries:
        suggest_query_terms = suggest_query.lower().split()
        if set(query_terms).intersection(set(suggest_query_terms)):
            freq = sum([query_freq[term] for term in set(query_terms) & set(suggest_query_terms)])
            suggestions.append((suggest_query, freq))

    return suggestions

def _get_ranked_suggestion(suggestions: list) -> list:
    ranked_suggestions = sorted(suggestions, key=lambda x: -x[1])
    return [suggestion[0] for suggestion in ranked_suggestions]

def _suggest_corrected_query(text: str):
    spell = SpellChecker()
    word_set = set(words.words())
    corrected_tokens = []

    for token in text.split():
        if token in word_set:
            corrected_tokens.append(token)
        else:
            suggestions = spell.candidates(token)
            if suggestions:
                corrected_tokens.append(spell.correction(token))
            else:
                corrected_tokens.append(token)

    return ' '.join(corrected_tokens)

def get_ranked_query_suggestions(query: str, dataset_name: str):
    corrected_query = _suggest_corrected_query(query)
    suggestions = _get_query_suggestions(corrected_query, dataset_name)
    ranked_suggestions = _get_ranked_suggestion(suggestions)
    ranked_suggestions.insert(0, corrected_query)
    return ranked_suggestions[:15]

__all__ = ['set_query_refinement_global_variables', 'get_ranked_query_suggestions', 'initialize_queries_db', 'index_query']
