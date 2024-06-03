import time

import ir_datasets

from matching_ranking import ranking

# git rm -r --cached C:\\Users\\ARWAA\\Desktop\\IR3\\db
# git rm -r --cached C:\\Users\\ARWAA\\Desktop\\IR3\\db10
# git rm -r --cached C:\\Users\\ARWAA\\Desktop\\IR3\\db100
# git rm -r --cached C:\\Users\\ARWAA\\Desktop\\IR3\\db200
# git rm -r --cached C:\\Users\\ARWAA\\Desktop\\IR3\\wiki
# echo "C:\\Users\\ARWAA\\Desktop\\IR3\\db10" >> .gitignore

# def _get_docs_store(dataset: str):
#     if dataset == "technology":
#         return ir_datasets.load("lotte/technology/test").docs_store()
#     else:
#         return ir_datasets.load("beir/quora/test").docs_store()
import pandas as pd

def _get_docs_store(dataset: str):
    if dataset == "antique":
        file_path = "C:\\Users\\ARWAA\\.ir_datasets\\antique\\collection.tsv"
    else:  # assuming dataset == "quora"
        file_path = "C:\\Users\\ARWAA\\Desktop\\IR3\\wiki\\documents.tsv"

    # Load the TSV file into a pandas DataFrame
    docs_store = pd.read_csv(file_path, sep='\t', header=None, names=['doc_id', 'doc_content'])
    
    # Convert DataFrame to a dictionary with doc_id as the key and doc_content as the value
    docs_store = dict(zip(docs_store['doc_id'], docs_store['doc_content']))
    
    return docs_store

# def _get_full_docs_content(docs: list, dataset: str):
#     docs_store = _get_docs_store(dataset)
#     return docs_store.get_many(docs)

def _get_full_docs_content(docs: list, dataset: str):
    docs_store = _get_docs_store(dataset)
    
    # الحصول على المعرّفات مع المحتوى
    full_docs_content = [{'id': doc_id, 'text': docs_store.get(doc_id)} for doc_id in docs]
    
    return full_docs_content



# def _get_ordered_full_docs(docs: list, full_docs: dict):
#     return {doc_id: full_docs[doc_id] for doc_id in docs if doc_id in full_docs}



def _get_ordered_full_docs(docs: list, full_docs: list):
    # تحويل قائمة القواميس إلى قاموس معرّف
    full_docs_dict = {doc['id']: doc for doc in full_docs}
    
    # إعادة ترتيب المستندات بالترتيب المطلوب
    return {doc_id: full_docs_dict[doc_id] for doc_id in docs if doc_id in full_docs_dict}




def _get_sliced_results_template(ordered_full_docs: dict) -> dict:
    total_result = [{'id': doc_id, 'text': doc['text']} for doc_id, doc in ordered_full_docs.items()]

    # total_result = [{'id': doc_id, 'text': doc.text} for doc_id, doc in ordered_full_docs.items()]
    sliced_result = total_result[:10]
    return {"results": sliced_result, "result_count": len(total_result)}


def ranking_call(retrieving_relevant_on: str, query: str, dataset: str) -> list:
    return list(ranking(query, dataset).keys())


def get_search_result(query: str, dataset: str, retrieving_relevant_on: str) -> dict:
    start_time = time.time()
    docs = ranking_call(retrieving_relevant_on, query, dataset)
    print(docs[:20])
    full_docs = _get_full_docs_content(docs, dataset)
    # ordered_full_docs = _get_ordered_full_docs(docs, full_docs)
    ordered_full_docs = _get_ordered_full_docs(docs, full_docs)
    # print("ordered_full_docs",ordered_full_docs)
    response = _get_sliced_results_template(ordered_full_docs)
    end_time = time.time()
    # append elapsed time to response
    response["elapsed_time"] = end_time - start_time
    return response


__all__ = ["get_search_result"]

# ['727663_0', '4384685_18', '4384685_22', '727663_3', '4384685_57', 
# '260258_2', '727663_5', '727663_1', '4384685_14', '3233772_1', '4384685_3',
#  '4384685_39', '4384685_67', '147794_4',
#  '4384685_4', '2986686_1', '1979626_1', '4384685_38', '4384685_25', '1979626_0']
#  'result_count': 38, 'elapsed_time': 1.655583143234253}

# ['4309481_7', '727663_0', '3419200_0', '1874124_2', '1400883_3', '365283_4', 
# '4384685_18', '4388183_13', '1822339_1', '1498260_7', '1681920_0', '1703485_5', 
# '3806718_2', '4384685_22',
#  '2025828_8', '4309481_5', '2339723_4', '260258_2', '2300357_6', '3760593_0']


