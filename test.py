from search import get_search_result
from inverted_index import set_inverted_index_store_global_variables

def search():
    # query = request.args.get('query')
    # dataset = request.args.get('dataset')
    # retrieving_relevant_on = "terms"  # "terms" or "topics"
    query="What do i do about not wanting to sleep at night?"
    dataset ="antique"
    retrieving_relevant_on = "terms"
    return get_search_result(query, dataset, retrieving_relevant_on)
set_inverted_index_store_global_variables()
print(search())

def search1():
    # query = request.args.get('query')
    # dataset = request.args.get('dataset')
    # retrieving_relevant_on = "terms"  # "terms" or "topics"
    query="arm architecture"
    dataset ="wiki"
    retrieving_relevant_on = "terms"
    return get_search_result(query, dataset, retrieving_relevant_on)
# set_inverted_index_store_global_variables()
# print(search1())
