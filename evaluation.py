# from typing import Dict
# import pandas as pd
# import os
# from inverted_index import set_inverted_index_store_global_variables
# from matching_ranking import ranking


# def get_queries_corpus(file_path: str) -> Dict[str, str]:
#     queries_df = pd.read_csv(file_path, sep='\t', header=None, names=['query_id', 'query_text'])
#     queries_df['query_id'] = queries_df['query_id'].astype(str)
#     queries_corpus = dict(zip(queries_df['query_id'], queries_df['query_text']))
#     return queries_corpus


# def compute_metrics(ranked_docs, qrels, k=None):
#     metrics = {}

#     ap_sum = 0
#     mrr_sum = 0
#     p10_sum = 0
#     overall_precision = 0
#     overall_recall = 0
#     overall_f1_score = 0

#     for query_id in ranked_docs.keys():
#         if query_id not in qrels:
#             print(f"Warning: {query_id} not found in qrelsMap")
#             continue

#         ranked_list = ranked_docs[query_id]
#         relevant_docs = [doc_id for doc_id, score in qrels[query_id].items() if score > 0]

#         if k is not None:
#             ranked_list = {key: value for key, value in list(ranked_list.items())[:k]}

#         tp = len(set(ranked_list).intersection(set(relevant_docs)))
#         precision = tp / len(ranked_list) if len(ranked_list) > 0 else 0
#         recall = tp / len(relevant_docs) if len(relevant_docs) > 0 else 0
#         f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

#         overall_precision += precision
#         overall_recall += recall
#         overall_f1_score += f1_score

#         ap_num = 0
#         for x in range(len(ranked_list)):
#             act_set = set(relevant_docs)
#             pred_set = set(list(ranked_list)[:x+1])
#             precision_at_k = len(act_set & pred_set) / (x + 1)
#             rel_k = 1 if list(ranked_list.keys())[x] in relevant_docs else 0
#             ap_num += precision_at_k * rel_k

#         ap = ap_num / len(relevant_docs) if len(relevant_docs) > 0 else 1
#         ap_sum += ap
#         p10 = len(set(list(ranked_list)[:10]).intersection(set(relevant_docs)))
#         p10_sum += p10 / 10

#         metrics[query_id] = {
#             'precision': precision,
#             'recall': recall,
#             'f1_score': f1_score,
#             'ap': ap,
#             'p10': p10
#         }

#     overall_precision = overall_precision / len(ranked_docs) if len(ranked_docs) > 0 else 0
#     overall_recall = overall_recall / len(ranked_docs) if len(ranked_docs) > 0 else 0
#     overall_f1_score = overall_f1_score / len(ranked_docs) if len(ranked_docs) > 0 else 0
#     overall_ap = ap_sum / len(ranked_docs) if len(ranked_docs) > 0 else 0
#     overall_mrr = mrr_sum / len(ranked_docs) if len(ranked_docs) > 0 else 0
#     overall_p10 = p10_sum / len(ranked_docs) if len(ranked_docs) > 0 else 0

#     metrics['overall'] = {
#         'precision': overall_precision,
#         'recall': overall_recall,
#         'f1_score': overall_f1_score,
#         'map': overall_ap,
#         'mrr': overall_mrr,
#         'p10': overall_p10
#     }

#     return metrics["overall"]


# def get_qrels(file_path: str):
#     qrels_df = pd.read_csv(file_path, sep=r'\s+', header=None, names=['query_id', 'Q0', 'doc_id', 'relevance'])
#     qrels_df = qrels_df.drop(columns=['Q0'])
#     qrels_df['query_id'] = qrels_df['query_id'].astype(str)
#     qrels_df['doc_id'] = qrels_df['doc_id'].astype(str)
#     qrels = qrels_df.to_dict('records')
#     return qrels


# def evaluate(dataset: str, dataset_name: str, k=None):
#     qrelsMap = {}
#     qrels = []
#     if dataset_name == 'antique':
#         file_path = os.path.join('C:\\Users\\ARWAA\\.ir_datasets', 'antique', 'antique-train.qrel')
#         qrels = get_qrels(file_path)
#     elif dataset_name == 'wiki':
#         file_path = os.path.join('C:\\Users\\User\\Desktop\\wikIR1k', 'training', 'qrels')
#         qrels = get_qrels(file_path)

#     for qrel in qrels:
#         query_id = qrel['query_id']
#         if query_id in qrelsMap:
#             qrelsMap[query_id].update({qrel['doc_id']: qrel['relevance']})
#         else:
#             qrelsMap[query_id] = {qrel['doc_id']: qrel['relevance']}

#     ranked_docs = {}
#     if dataset_name == 'antique':
#         file_path1 = os.path.join('C:\\Users\\ARWAA\\.ir_datasets', 'antique', 'processed_queries.tsv')
#         queries = get_queries_corpus(file_path1)
#     elif dataset_name == 'wiki':
#         file_path1 = os.path.join('C:\\Users\\User\\Desktop\\IR33 - Copy', 'cleaned_queries.tsv')
#         queries = get_queries_corpus(file_path1)

#     for query_id in queries.keys():
#         results = ranking(queries[query_id], dataset_name)
#         results = {str(doc_id): score for doc_id, score in results.items()}
#         ranked_docs[query_id] = results
#         print(f"currently ranking {query_id}")

#     evaluation = compute_metrics(ranked_docs, qrelsMap, k)
#     print(evaluation)


# set_inverted_index_store_global_variables()
# print("antique evaluation")
# evaluate("beir/quora/test", "antique")

from typing import Dict
import pandas as pd
from inverted_index import set_inverted_index_store_global_variables
from matching_ranking import ranking


def __get_queries_corpus1(file_path: str) -> Dict[str, str]:# from matching_ranking import ranking

    queries_df = pd.read_csv(file_path, sep='\t', header=None, names=['query_id', 'query_text'])
    # تحويل المعرفات إلى نصوص
    queries_df['query_id'] = queries_df['query_id'].astype(str)
    queries_corpus = dict(zip(queries_df['query_id'], queries_df['query_text']))
    return queries_corpus

def compute_metrics(ranked_docs, qrels, k=None):
    metrics = {}
    ap_sum = 0
    mrr_sum = 0
    p10_sum = 0
    overall_precision = 0
    overall_recall = 0
    overall_f1_score = 0

    for query_id in ranked_docs.keys():
        if query_id not in qrels:
            print(f"Warning: {query_id} not found in qrelsMap")
            continue

        ranked_list = ranked_docs[query_id]
        relevant_docs = [doc_id for doc_id, score in qrels[query_id].items() if score > 0]

        if k is not None:
            ranked_list = {key: value for key, value in list(ranked_list.items())[:k]}

        tp = len(set(ranked_list).intersection(set(relevant_docs)))
        precision = tp / len(ranked_list) if len(ranked_list) > 0 else 0
        recall = tp / len(relevant_docs) if len(relevant_docs) > 0 else 0
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        overall_precision += precision
        overall_recall += recall
        overall_f1_score += f1_score

        ap = 0
        relevant_docs_seen = set()
        for i, doc_id in enumerate(ranked_list):
            if doc_id in relevant_docs and doc_id not in relevant_docs_seen:
                ap += (len(relevant_docs_seen) + 1) / (i + 1)
                relevant_docs_seen.add(doc_id)
                if len(relevant_docs_seen) == 1:
                    mrr_sum += 1 / (i + 1)
                if len(relevant_docs_seen) == len(relevant_docs):
                    break

        ap /= len(relevant_docs) if len(relevant_docs) > 0 else 1
        ap_sum += ap
        p10 = len(set(list(ranked_list)[:10]).intersection(set(relevant_docs)))
        p10_sum += p10 / 10

        metrics[query_id] = {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'ap': ap,
            'p10': p10
        }
        
#####################################################3
        # طباعة القيم لكل استعلام
        # print(f"Metrics for query {query_id}: Precision: {precision}, Recall: {recall}, F1 Score: {f1_score}, AP: {ap}, P10: {p10}")

    overall_precision = overall_precision / len(ranked_docs)
    overall_recall = overall_recall / len(ranked_docs)
    overall_f1_score = overall_f1_score / len(ranked_docs)
    overall_ap = ap_sum / len(ranked_docs)
    overall_mrr = mrr_sum / len(ranked_docs)
    overall_p10 = p10_sum / len(ranked_docs)

    metrics['overall'] = {
        'precision': overall_precision,
        'recall': overall_recall,
        'f1_score': overall_f1_score,
        'map': overall_ap,
        'mrr': overall_mrr,
        'p10': overall_p10
    }

    return metrics["overall"]



def _get_qrels(file_path: str):
    qrels_df = pd.read_csv(file_path, sep=r'\s+', header=None, names=['query_id', 'Q0', 'doc_id', 'relevance'])
    qrels_df = qrels_df.drop(columns=['Q0'])
    # تحويل المعرفات إلى نصوص
    qrels_df['query_id'] = qrels_df['query_id'].astype(str)
    qrels_df['doc_id'] = qrels_df['doc_id'].astype(str)
    qrels = qrels_df.to_dict('records')
    return qrels

def evaluate(dataset: str, dataset_name: str, k=None):
    qrelsMap = {}
    qrels = []
    if dataset_name == 'antique':
        file_path = 'C:\\Users\\ARWAA\\.ir_datasets\\antique\\antique-train.qrel'
        # file_path="C:\\Users\\ARWAA\\Desktop\\IR3\\antique-test.qrel"
        qrels = _get_qrels(file_path)

    if dataset_name == 'wiki':
        file_path = "C:\\Users\\ARWAA\\Desktop\\IR3\\wiki\\qrels"
        qrels = _get_qrels(file_path)

    for qrel in qrels:
        query_id = qrel['query_id']  # الآن query_id هو نص
        if query_id in qrelsMap:
            qrelsMap[query_id].update({qrel['doc_id']: qrel['relevance']})
        else:
            qrelsMap[query_id] = {qrel['doc_id']: qrel['relevance']}

    ranked_docs = {}
    if dataset_name == 'antique':
        file_path1 = "C:\\Users\\ARWAA\\.ir_datasets\\antique\\processed_queries.tsv"
        # file_path1 = "C:\\Users\\ARWAA\\Desktop\\IR3\\antique-test-queries.tsv" 
        queries = __get_queries_corpus1(file_path1)
    if dataset_name == 'wiki':
        
        file_path1 = "C:\\Users\\ARWAA\\Desktop\\IR3\\wiki\\cleaned_queries.tsv"
        queries = __get_queries_corpus1(file_path1)

    for query_id in queries.keys():
        results = ranking(queries[query_id], dataset_name)
        # تحويل معرفات الوثائق إلى نصوص
        results = {str(doc_id): score for doc_id, score in results.items()}
        ranked_docs[query_id] = results
        print(f"currently ranking {query_id}")

    evaluation = compute_metrics(ranked_docs, qrelsMap, k)
    print(evaluation)

set_inverted_index_store_global_variables()
# print("wiki evaluation")
# evaluate("beir/quora/test", "wiki")

print("antique evaluation")
evaluate("beir/quora/test", "antique")