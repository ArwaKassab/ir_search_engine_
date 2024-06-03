
from inverted_index import set_inverted_index_store_global_variables
from query_refinement import set_query_refinement_global_variables, initialize_queries_db

# إعداد المتغيرات العالمية لمؤشر معكوس
try:
    set_inverted_index_store_global_variables()
except KeyError as e:
    print(f"Error: {e} key not found in the shelve database.")

# إعداد المتغيرات العالمية لتحسين الاستعلامات
try:
    initialize_queries_db()
    set_query_refinement_global_variables()
except Exception as e:
    print(f"Error initializing query refinement variables: {e}")
