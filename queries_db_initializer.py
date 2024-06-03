# from query_refinement import initialize_queries_db,set_inverted_index_store_global_variables,set_query_refinement_global_variables

# initialize_queries_db()
# print("Queries DB initialized successfully")

# init.py
# setup.py
# setup.py
# from inverted_index import set_inverted_index_store_global_variables
# from query_refinement import set_query_refinement_global_variables, initialize_queries_db

# def setup_inverted_index():
#     try:
#         set_inverted_index_store_global_variables()
#     except KeyError as e:
#         print(f"Error: {e} key not found in the shelve database.")
#         # يمكنك إضافة معالجة أخرى للأخطاء هنا أو إنهاء البرنامج

# def setup_query_refinement():
#     try:
#         initialize_queries_db()
#         set_query_refinement_global_variables()
#     except Exception as e:
#         print(f"Error initializing query refinement variables: {e}")
#         # يمكنك إضافة معالجة أخرى للأخطاء هنا أو إنهاء البرنامج
# setup.py
# setup.py
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
