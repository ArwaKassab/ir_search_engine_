import shelve
from collections import defaultdict
from inverted_index import get_weighted_inverted_index , set_inverted_index_store_global_variables


import csv
from inverted_index import get_weighted_inverted_index, set_inverted_index_store_global_variables


def save_inverted_index_to_tsv(dataset_name: str, output_file: str) -> None:

   
    weighted_inverted_index = get_weighted_inverted_index(dataset_name)

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        tsv_writer = csv.writer(file, delimiter='\t')
        tsv_writer.writerow(['Term', 'Document ID', 'Weight'])  # كتابة العنوان
        for term, postings in weighted_inverted_index.items():

            for posting in postings:

                if isinstance(posting, dict) and len(posting) == 1:  
                    doc_id, weight = next(iter(posting.items()))  
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

