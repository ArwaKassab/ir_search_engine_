import shelve
from collections import defaultdict


def merge_inverted_indices(dataset_name_1: str, dataset_name_2: str, merged_dataset_name: str) -> None:
    with shelve.open('db/' + dataset_name_1 + '_inverted_index.db') as db1, \
         shelve.open('db/' + dataset_name_2 + '_inverted_index.db') as db2, \
         shelve.open('db/' + merged_dataset_name + '_inverted_index.db', 'n') as db_merged:

        # التأكد من وجود المفتاح 'inverted_index'
        if 'inverted_index' not in db1:
            raise KeyError(f"المفتاح 'inverted_index' غير موجود في قاعدة البيانات '{dataset_name_1}'")
        if 'inverted_index' not in db2:
            raise KeyError(f"المفتاح 'inverted_index' غير موجود في قاعدة البيانات '{dataset_name_2}'")

        index1 = db1['inverted_index']
        index2 = db2['inverted_index']
        
        merged_index = defaultdict(list)
        for term in set(index1.keys()).union(set(index2.keys())):
            merged_index[term].extend(index1.get(term, []) + index2.get(term, []))
        
        db_merged['inverted_index'] = merged_index
        print("تم دمج الفهارس بنجاح")



def merge_docs_vectors(dataset_name_1: str, dataset_name_2: str, merged_dataset_name: str) -> None:
    db1_path = 'db/' + dataset_name_1 + '_documents_vector.db'
    db2_path = 'db/' + dataset_name_2 + '_documents_vector.db'
    db_merged_path = 'db/' + merged_dataset_name + '_documents_vector.db'
   

    with shelve.open(db1_path) as db1, \
         shelve.open(db2_path) as db2, \
         shelve.open(db_merged_path, 'n') as db_merged:

        vectors1 = db1['documents_vector']
        vectors2 = db2['documents_vector']
        
        merged_vectors = {**vectors1, **vectors2}
        
        db_merged['documents_vector'] = merged_vectors

    print(f"تم دمج ملفات docs_vectors في '{merged_dataset_name}_documents_vector.db'")

merge_inverted_indices('antique1', 'antique2', 'antique')
merge_docs_vectors('antique1', 'antique2', 'antique')
__all__ = ['merge_inverted_indices', 'merge_docs_vectors']