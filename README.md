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

- *Data Processing*:

   The implemented text processing steps are:

   1. _expand_abbreviations
   
   2. Normalize dates
   
   2. nltk.word_tokenize
   
   3. _filter_tokens
   
   4. Stemming
   
   5. lemmatize
   
   6. _remove_punctuations

- *Create Inverted Index*:
   Gets the weighted inverted index for the given dataset.
  
- *Ranking&ةmatching*:
   Performs a query search and returns ranked documents.

 - *Search*:
   Performs search query and get full documnents results based on passed   
   query and dataset passed.

- *Query Processing*
- *Evaluation*:
   The implemented evaluation metrics are Precision, Recall, MAP, MRR and 
   Precision@10.
   to run the evaluation just go to evaluation.py file and run it.

- *EXTRA*:
   1-Query Suggestions & Correction_suggestion
   2-Crawling


## Students

- [Aya Barnia]
- [Arwa Kassab]
- [Raneem Kharboutly]
- [Ahed Asaad]
