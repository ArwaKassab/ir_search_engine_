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



file_path = 'C:\\Users\\ARWAA\\.ir_datasets\\antique\\processed_collection.tsv'

df = pd.read_csv(file_path, sep='\t', header=None, names=['doc_id', 'doc_content'])

antique = dict(zip(df['doc_id'], df['doc_content']))
create_weighted_inverted_index_from_tsv(antique, 'antique')


file_path = "C:\\Users\\ARWAA\\Desktop\\IR3\\wiki\\cleaned_documents.tsv"
df = pd.read_csv(file_path, sep='\t', header=None, names=['doc_id', 'doc_content'])
wiki = dict(zip(df['doc_id'], df['doc_content']))
create_weighted_inverted_index_from_tsv(wiki, 'wiki')



create_queries_unweighted_inverted_index("antique")
create_queries_unweighted_inverted_index("wiki")

set_inverted_index_store_global_variables()
print('done')
