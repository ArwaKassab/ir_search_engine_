from search import get_search_result
from inverted_index import set_inverted_index_store_global_variables

def search():
    query="What do i do about not wanting to sleep at night?"
    dataset ="antique"
    return get_search_result(query, dataset,)
set_inverted_index_store_global_variables()
print(search())

def search1():

    query="arm architecture"
    dataset ="wiki"
    return get_search_result(query, dataset)
