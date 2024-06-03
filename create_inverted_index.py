import pandas as pd
import shelve
import math
import shelve
from collections import defaultdict
from typing import Dict
import pandas as pd

import ir_datasets
from inverted_index import create_weighted_inverted_index_from_tsv , get_weighted_inverted_index , get_document_vector,get_documents_vector ,set_inverted_index_store_global_variables , create_crawled_content_index_from_tsv
from query_processing import create_unweighted_inverted_index as create_queries_unweighted_inverted_index , _get_unweighted_inverted_index as get_unweighted_queries_inverted_index

data = 'C:\\Users\\ARWAA\\.ir_datasets\\antique\\processed_collection.tsv'


dataset_name='antique'


# # creating documents inverted indexes
# create_weighted_inverted_index_from_tsv(data,dataset_name)
# print("finished creating technology index")


# def display_documents_vector(dataset_name):
#     # Open the shelve file
#     with shelve.open('db/' + dataset_name + '_documents_vector.db') as db:
#         # Get the documents vector
#         documents_vector = db.get('documents_vector', {})

#         # # Display the documents vector
#         for doc_id, vector in documents_vector.items():
#             print(f"Document ID: {doc_id}")
#             print("Vector:")
#             for term, weight in vector.items():
#                 print(f"   Term: {term}, Weight: {weight}")
#         # for doc_id, vector in documents_vector.items():
#         #     print(f"Document ID: {doc_id}")
#         #     for term, tfidf in vector.items():
#         #         print(f"\t{term}: {tfidf}")

# display_documents_vector('antique')
# set_inverted_index_store_global_variables()
# create_queries_unweighted_inverted_index("antique")
# unweighted_queries_inverted_index = get_unweighted_queries_inverted_index('antique')


# create_queries_unweighted_inverted_index("antique")
# print("finished creating technology queries index")

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



# import shelve
# from collections import defaultdict



# import shelve
# from collections import defaultdict
# from typing import Dict

# def store_docs_vectors(dataset_name: str, vectors: Dict[str, Dict[str, float]]) -> None:
#     with shelve.open('db/' + dataset_name + '_docs_vectors.db') as db:
#         db['docs_vectors'] = vectors
#     print(f"تم حفظ ملفات docs_vectors في '{dataset_name}_docs_vectors.db'")

# def create_weighted_inverted_index_from_tsv(corpus: Dict[str, str], dataset_name: str) -> None:
#     weighted_inverted_index = defaultdict(list)
#     vectors = _create_docs_vectors(corpus, dataset_name)
    
#     # تخزين docs_vectors
#     store_docs_vectors(dataset_name, vectors)
    
#     for doc_id, doc_weighted_terms in vectors.items():
#         for term, weight in doc_weighted_terms.items():
#             weighted_inverted_index[term].append({doc_id: weight})
    
#     store_weighted_inverted_index(dataset_name, weighted_inverted_index)

# ///////////////////////////////////////////////////////////////////////////////////////////////

file_path = 'C:\\Users\\ARWAA\\.ir_datasets\\antique\\processed_collection.tsv'

df = pd.read_csv(file_path, sep='\t', header=None, names=['doc_id', 'doc_content'])
# قراءة الملف ومعالجة ثاني 100,000 وثيقة
antique = dict(zip(df['doc_id'][300000:400000], df['doc_content'][300000:400000]))
create_weighted_inverted_index_from_tsv(antique, 'antique')


# file_path = "C:\\Users\\ARWAA\\Desktop\\IR3\\wiki\\cleaned_documents.tsv"
# df = pd.read_csv(file_path, sep='\t', header=None, names=['doc_id', 'doc_content'])
# wiki = dict(zip(df['doc_id'][0:10000], df['doc_content'][0:10000]))
# create_weighted_inverted_index_from_tsv(wiki, 'wiki')


# file_path = "C:\\Users\\ARWAA\\Desktop\\IR3\\wiki\\cleaned_documents.tsv"
# # قراءة الملف مع تحديد نوع البيانات للعمود 'doc_id' وضبط low_memory=False
# df = pd.read_csv(file_path, sep='\t', header=None, names=['doc_id', 'doc_content'], dtype={'doc_id': str}, low_memory=False)
# # إنشاء القاموس من الأجزاء المطلوبة من البيانات
# wiki = dict(zip(df['doc_id'][0:10000], df['doc_content'][0:10000]))
# create_weighted_inverted_index_from_tsv(wiki, 'wiki')

# def merge_inverted_indices(dataset_name_1: str, dataset_name_2: str, merged_dataset_name: str) -> None:
#     with shelve.open('db/' + dataset_name_1 + '_inverted_index.db') as db1, \
#          shelve.open('db/' + dataset_name_2 + '_inverted_index.db') as db2, \
#          shelve.open('db/' + merged_dataset_name + '_inverted_index.db', 'n') as db_merged:

#         # التأكد من وجود المفتاح 'inverted_index'
#         if 'inverted_index' not in db1:
#             raise KeyError(f"المفتاح 'inverted_index' غير موجود في قاعدة البيانات '{dataset_name_1}'")
#         if 'inverted_index' not in db2:
#             raise KeyError(f"المفتاح 'inverted_index' غير موجود في قاعدة البيانات '{dataset_name_2}'")

#         index1 = db1['inverted_index']
#         index2 = db2['inverted_index']
        
#         merged_index = defaultdict(list)
#         for term in set(index1.keys()).union(set(index2.keys())):
#             merged_index[term].extend(index1.get(term, []) + index2.get(term, []))
        
#         db_merged['inverted_index'] = merged_index
#         print("تم دمج الفهارس بنجاح")

# # استدعاء الدالة مع التأكد من وجود قواعد البيانات
# merge_inverted_indices('antique', 'dataset_therd_100k', 'antique1')
# print('done')


# def merge_docs_vectors(dataset_name_1: str, dataset_name_2: str, merged_dataset_name: str) -> None:
#     db1_path = 'db/' + dataset_name_1 + '_documents_vector.db'
#     db2_path = 'db/' + dataset_name_2 + '_documents_vector.db'
#     db_merged_path = 'db/' + merged_dataset_name + '_documents_vector.db'
   

#     with shelve.open(db1_path) as db1, \
#          shelve.open(db2_path) as db2, \
#          shelve.open(db_merged_path, 'n') as db_merged:

#         vectors1 = db1['documents_vector']
#         vectors2 = db2['documents_vector']
        
#         merged_vectors = {**vectors1, **vectors2}
        
#         db_merged['documents_vector'] = merged_vectors

#     print(f"تم دمج ملفات docs_vectors في '{merged_dataset_name}_documents_vector.db'")

# merge_docs_vectors('antique', 'dataset_therd_100k', 'antique1')


create_queries_unweighted_inverted_index("antique")
# create_queries_unweighted_inverted_index("wiki")
# # print("finished creating antique queries index")

set_inverted_index_store_global_variables()
print('done')
