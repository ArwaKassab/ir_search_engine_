import shelve
from collections import defaultdict
from inverted_index import get_weighted_inverted_index , set_inverted_index_store_global_variables


import csv
from inverted_index import get_weighted_inverted_index, set_inverted_index_store_global_variables


def save_inverted_index_to_tsv(dataset_name: str, output_file: str) -> None:
    # الحصول على الفهرس المعكوس للبيانات المحددة
   
    weighted_inverted_index = get_weighted_inverted_index(dataset_name)
    
    # عبارات الطباعة للمساعدة في تصحيح الأخطاء
    # print(f"Weighted Inverted Index: {weighted_inverted_index}")

    # حفظ الفهرس المعكوس في ملف TSV
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        tsv_writer = csv.writer(file, delimiter='\t')
        tsv_writer.writerow(['Term', 'Document ID', 'Weight'])  # كتابة العنوان
        for term, postings in weighted_inverted_index.items():
            # print(f"Processing term: {term} with postings: {postings}")
            for posting in postings:
                # print(f"Processing posting: {posting}")
                if isinstance(posting, dict) and len(posting) == 1:  # التحقق من أن العنصر عبارة عن قاموس يحتوي على عنصر واحد
                    doc_id, weight = next(iter(posting.items()))  # استخراج المعرّف والوزن
                    tsv_writer.writerow([term, doc_id, weight])
                else:
                    print(f"Skipping invalid posting: {posting}")


def print_inverted_index_from_tsv(input_file: str) -> None:
    # قراءة وطباعة الفهرس المعكوس من ملف TSV
    with open(input_file, 'r', encoding='utf-8') as file:
        tsv_reader = csv.reader(file, delimiter='\t')
        next(tsv_reader)  # تخطي العنوان
        for row in tsv_reader:
            term, doc_id, weight = row
            print(f"Term: {term}, Document ID: {doc_id}, Weight: {weight}")

set_inverted_index_store_global_variables()
# مثال على الاستخدام
dataset_name = 'antique'
output_file = 'antique_100_new .tsv'

save_inverted_index_to_tsv(dataset_name, output_file)
print_inverted_index_from_tsv(output_file)


# def print_inverted_index(dataset_name: str) -> None:
#     with shelve.open(f'db/{dataset_name}_inverted_index.db') as db:
#         inverted_index = db['inverted_index']
#         for term, postings in inverted_index.items():
#             print(f"Term: {term}")
#             # for posting in postings:
#             #     for doc_id, weight in posting.items():
#             #         print(f"\tDocument ID: {doc_id}, Weight: {weight}")

# # Example usage
# print_inverted_index('antique_queries')

# self.assertEqual(_antique_weighted_inverted_index, {'term1': [1, 2], 'term2': [2, 3]})
# self.assertEqual(_antique_documents_vector, {1: [0.1, 0.2], 2: [0.2, 0.3]})
       


# import shelve

# # Check the contents of the shelve file
# with shelve.open('db/antique_inverted_index.db') as db:
#     print('antique_inverted_index:', db.get('inverted_index', 'Key not found'))

# with shelve.open('db/antique_documents_vector.db') as db:
#     print('antique_documents_vector:', db.get('documents_vector', 'Key not found'))
# set_inverted_index_store_global_variables()

# weighted_inverted_index = get_weighted_inverted_index('antique')

# if weighted_inverted_index is not None:
#     print(f"Weighted inverted index for dataset {'wiki'}:")
# else:
#     print("Error: Weighted inverted index is None.")



