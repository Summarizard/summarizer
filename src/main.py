from summarizer import get_summary, get_tags

# Function which summarizes and extracts information from a given text
#   text: Text which you want to summarize
#   sentences: Number of sentences that will be extracted from text
#   tags: Number of tags that will be extracted from text
#   lang: Language of the text
# Returns an array
#   0: Array of summarized text of <sentences> sentences
#   1: Array of <tags> tags extracted from given text
#   2: Cleaned given text
def summarize(text, sentences = 5, tags = 5, lang = "en"):
    [summary, tags] = get_summary(text, lang, sentences, tags)
    return [summary, tags, text]
