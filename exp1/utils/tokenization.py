from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


sentence = """
    I am superman, but I want to be the Peter Pan.
    USTC is the best university in Hefei.
    """
tokens = word_tokenize(sentence)

tokensFiltered = []
stopWords = set(stopwords.words('english'))

for token in tokens:
    if token not in stopWords:
        tokensFiltered.append(token)

print(tokens)
print(tokensFiltered)