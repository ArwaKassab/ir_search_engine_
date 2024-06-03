# Information Retrieval System

***

A university project that uses two datasets from [ir-datasets](https://ir-datasets.com/) and build a search engine on them using Python.

## Datasets

- [antique](https://ir-datasets.com/antique.html#antique/train).

- [wikir](https://ir-datasets.com/wikir.html#wikir/en1k).


## How to run the project?

Install required packages. 

Run create_inverted_index.py file for the first time to set the database on your device.


## How to use the search engine?


Running *search* by running main.py to try the search engine.



## Services


- Search:

Performs search query and get full documnents results based on passed query and dataset passed.



- Text Processing:

The implemented text processing steps are:

1. _expand_abbreviations

2. Normalize dates

2. nltk.word_tokenize

3. _filter_tokens

4. Stemming

5. lemmatize

6. _remove_punctuations


- Ranking:

Performs a query search and returns ranked documents. 



- Get Inverted Index:

Gets the weighted inverted index for the given dataset. 



- Create Inverted Index:

Creates the weighted inverted index for the given dataset. 



- Get Document Vector:

Gets the document vector for the given document and dataset. 



 

- Get Documents Vector:

Gets the documents vector for the given dataset. 



- Get Query TF-IDF:

Calculates the query TF-Idf for the given query and dataset. 

the following API runs the Get Documents Vector service:

    - GET: /query-tfidf?query="YOUR-QUERY"&dataset="quora/technology"

- Query Suggestions (query_refinement Branch):

Performs a query suggestions search and returns ranked suggestions to the given query and dataset.

the following API runs the Query Suggestions service:

    - GET: /suggestions?query="YOUR-QUERY"&dataset="quora/technology"

- ## Evaluation:

The implemented evaluation metrics are Precision, Recall, F1_score, MAP, MRR and Precision@10.

to run the evaluation just go to evaluation.py file and run it.


## Students

- [Aya Barnia]
- [Arwa Kassab]
- [Raneem Kharboutly]
- [Ahed Asaad]
