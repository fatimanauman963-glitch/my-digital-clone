# My NLP study notes

## What NLP is
Natural Language Processing is about making computers work with human language: understanding it, searching it and generating it. In my NLP course I studied how text becomes numbers, how models learn from those numbers, and how modern systems like chatbots use them.

## From text to numbers
First, text is split into tokens (words or word pieces). Each token is mapped to a vector. Older methods like bag-of-words and TF-IDF count words and ignore their order and meaning. Word embeddings and sentence embeddings are better because they place words and sentences with similar meaning close together in vector space. So "car" and "automobile" end up near each other even though they share no letters.

## Embeddings and similarity
To compare two pieces of text I turn both into embeddings and measure cosine similarity, which is the angle between the two vectors. A score close to 1 means very similar meaning. This is called semantic or dense search. Its strength is paraphrases: a question can match an answer even when they share no words. Its weakness is exact rare terms such as a project name, which the embedding may blur.

## Transformers
The Transformer is the architecture behind modern language models. Its key idea is self-attention: every token looks at every other token and decides how much to pay attention to each one, so context is captured in parallel instead of word by word like older RNNs. Positional encoding adds the order of the words. A Transformer is made of stacked layers of attention and feed-forward networks.

## Encoder and decoder models
Encoder models such as BERT read the whole sentence in both directions and are good for understanding tasks: classification, embeddings, search. Decoder models such as GPT generate text one token at a time, looking only at the earlier tokens, so they are good for writing answers. Encoder-decoder models such as T5 read an input with the encoder and write an output with the decoder, which suits translation and summarisation.

## Fine-tuning
A pretrained model already knows general language. Fine-tuning continues training it on a smaller task-specific dataset so it adapts to that task, like a medical or legal domain. It is cheaper than training from scratch, but it needs good data and it can forget some general knowledge if done badly.

## Retrieval methods
BM25 is a keyword ranking method that improves on TF-IDF. It scores a document higher when it contains the query words, especially rare ones, and it accounts for document length. It is fast and great for exact terms but it misses paraphrases. Dense retrieval uses embeddings and is great for meaning but can miss exact rare words. Hybrid retrieval combines both rankings, for example with Reciprocal Rank Fusion, which gives each document a score of 1 divided by (60 plus its rank) from each list and adds them up. Documents that rank well in both lists rise to the top.

## RAG
Retrieval-Augmented Generation connects retrieval with a language model. The steps are: chunk the documents, index them, retrieve the best chunks for a question, and then give those chunks to the language model as context so it answers from them. This reduces made-up answers because the model is told to use only the retrieved context and to say it does not know when the answer is missing. I built my own digital clone chatbot using this exact pipeline.
