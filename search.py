import time

import ir_datasets

from matching_ranking import ranking

# git rm -r --cached C:\\Users\\ARWAA\\Desktop\\IR3\\db
# git rm -r --cached C:\\Users\\ARWAA\\Desktop\\IR3\\db10
# git rm -r --cached C:\\Users\\ARWAA\\Desktop\\IR3\\db100
# git rm -r --cached C:\\Users\\ARWAA\\Desktop\\IR3\\db200
# git rm -r --cached C:\\Users\\ARWAA\\Desktop\\IR3\\wiki
# echo "C:\\Users\\ARWAA\\Desktop\\IR3\\db10" >> .gitignore


import pandas as pd

def _get_docs_store(dataset: str):
    if dataset == "antique":
        file_path = "C:\\Users\\ARWAA\\.ir_datasets\\antique\\collection.tsv"
    else:  # assuming dataset == "quora"
        file_path = "C:\\Users\\ARWAA\\Desktop\\IR3\\wiki\\documents.tsv"


    docs_store = pd.read_csv(file_path, sep='\t', header=None, names=['doc_id', 'doc_content'])
    

    docs_store = dict(zip(docs_store['doc_id'], docs_store['doc_content']))
    
    return docs_store

def _get_full_docs_content(docs: list, dataset: str):
    docs_store = _get_docs_store(dataset)
    
    # الحصول على المعرّفات مع المحتوى
    full_docs_content = [{'id': doc_id, 'text': docs_store.get(doc_id)} for doc_id in docs]
    
    return full_docs_content




def _get_ordered_full_docs(docs: list, full_docs: list):

    full_docs_dict = {doc['id']: doc for doc in full_docs}
    
    return {doc_id: full_docs_dict[doc_id] for doc_id in docs if doc_id in full_docs_dict}




def _get_sliced_results_template(ordered_full_docs: dict) -> dict:
    total_result = [{'id': doc_id, 'text': doc['text']} for doc_id, doc in ordered_full_docs.items()]

    sliced_result = total_result[:10]
    return {"results": sliced_result, "result_count": len(total_result)}


def ranking_call( query: str, dataset: str) -> list:
    return list(ranking(query, dataset).keys())


def get_search_result(query: str, dataset: str) -> dict:
    start_time = time.time()
    docs = ranking_call( query, dataset)
    print(docs[:20])
    full_docs = _get_full_docs_content(docs, dataset)
    ordered_full_docs = _get_ordered_full_docs(docs, full_docs)
    response = _get_sliced_results_template(ordered_full_docs)
    end_time = time.time()
    response["elapsed_time"] = end_time - start_time
    return response


__all__ = ["get_search_result"]

