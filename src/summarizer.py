import spacy
from textpipe import doc as textpipeDoc
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

# Function that summarize given text and return most valuable sentences and extracted keywords
def get_summary(text, lang, max_sentences = 3, max_tags = 5):
    clean_text = textpipeDoc.Doc(text).clean
    doc = get_document(clean_text, lang)
    keywords = get_keywords(doc)
    normalized_keywords = get_normalized_tags(keywords)
    sentence_strength = get_sentence_strength(doc, keywords)
    return [
        nlargest(max_sentences, sentence_strength, key=sentence_strength.get),
        get_tags(keywords, max_tags)
    ]

# Function that count importance of sentences
def get_sentence_strength(doc, keywords):
    sentence_strength = {}
    for sentence in doc.sents:
        for word in sentence:
            if word.text in keywords.keys():
                if sentence in sentence_strength.keys():
                    sentence_strength[sentence] += keywords[word.text]
                else:
                    sentence_strength[sentence] = keywords[word.text]
    return sentence_strength

# Function that return most valuable keywords
def get_tags(keywords, max = 5):
    words = []
    for word in keywords.most_common(max):
        words.append(word[0])
    return words

# Function that extract keywords from document and count their occurrences
def get_keywords(doc):
    stop_words = list(STOP_WORDS)
    keywords = []
    tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if (token.text in stop_words or token.text in punctuation):
            continue
        if (token.pos_ in tag):
            keywords.append(token.text)
    return Counter(keywords)

# Function that normalize given keywords
def get_normalized_tags(keywords):
    freq = Counter(keywords).most_common(1)[0][1]
    for word in keywords.keys():
        keywords[word] = keywords[word] / freq
    return keywords

# Function that make spacy document from text and language
def get_document(text, lang):
    # todo: support more languages and make it configurable
    nlp = spacy.load('{}_core_web_md'.format(lang))
    return nlp(text)
