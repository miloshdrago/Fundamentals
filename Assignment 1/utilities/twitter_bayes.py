# Adjustment to Naive Bayes Classifier to use twitter_samples dataset from nltk


# dependencies
from nltk.corpus import twitter_samples
from nltk.classify import NaiveBayesClassifier
import nltk.classify.util
import nltk
import string
import re
import unicodedata


class Sanitizer(object):
    """
    Class for sanitizing twitter messages.

    @example        ```
                    sanitizer = Sanitizer()

                    with open('mytextfile.txt', 'r') as f:
                        for line in f:
                            print(sanitizer.sanitize(line))
                    ```

    @dependencies   nltk, string, re
    @author         Tycho Atsma <tycho.atsma@student.uva.nl>
    @file           Sanitizer.py
    @documentation  public
    @copyright      University of Amsterdam
    """
    punctuation = string.punctuation
    stopwords = nltk.corpus.stopwords
    Lemmatizer = nltk.stem.WordNetLemmatizer
    Tokenizer = nltk.tokenize.TweetTokenizer

    def __init__(self):
        """
        Constructor.
        """
        self.punctuation_table = dict((ord(char), None) for char in string.punctuation)
        self.lemmatizer = self.Lemmatizer()
        self.tokenizer = self.Tokenizer()

    def remove_punctuation(self, message):
        """
        Method to remove punctuation from a twitter message.
        @param  string  Twitter message.
        @return string
        """
        return message.translate(self.punctuation_table).strip()

    def remove_stopwords(self, message, language="english"):
        """
        Method to remove stopwords from a twitter message.
        @param  string  Twitter message.
        @param  string  Language of the stopwords (default: english).
        @return string
        """
        stops = self.stopwords.words(language)
        tokens = message.split()
        return " ".join([token for token in tokens if token not in stops]).strip()

    def remove_links(self, message):
        """
        Method to remove links from a twitter message.
        @param  string  Twitter message.
        @return string
        """
        # source: https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
        pattern = r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
        return re.sub(pattern, "", message).strip()

    def remove_usertags(self, message):
        """
        Method to remove usertags from a twitter message.
        @param  string  Twitter message.
        @return string
        """
        pattern = r"(\@\w*)"
        return re.sub(pattern, "", message).strip()

    def remove_hashtags(self, message):
        """
        Method to remove hashtags from a twitter message.
        @param  string  Twitter message.
        @return string
        """
        pattern = r"(\#\w*)"
        return re.sub(pattern, "", message).strip()

    def lemmatize(self, message):
        """
        Method to lemmatize a twitter message.
        @param  string  Twitter message.
        @return string
        """
        tokens = message.split()
        return " ".join([self.lemmatizer.lemmatize(token) for token in tokens])

    def tokenize(self, message):
        """
        Method to tokenize a twitter message.
        @param  string  Twitter message.
        @return string
        """
        return self.tokenizer.tokenize(message)

    def sanitize(self, message):
        """
        Method to sanitize a twitter message.
        @param  string  Twitter message.
        @return string
        """
        # 1. we need to normalize the message
        message = unicodedata.normalize("NFC", message.lower().encode('utf8').decode('utf8'))

        # 2. we need to get rid of specific types of tokens
        message = self.remove_links(message)
        message = self.remove_usertags(message)
        message = self.remove_hashtags(message)

        # 3. we need to get rid of language noise
        message = self.remove_punctuation(message)
        message = self.remove_stopwords(message)
        message = self.lemmatize(message)

        # 4. we need tokenize the message
        message = self.tokenize(message)

        # expose the sanitized message without single characters
        return [token for token in message if len(token) > 1]


sanitizer = Sanitizer()

# A function that extracts which words exist in a text based on a list of words to which we compare.


def word_feats(words):
    return dict([(word, True) for word in words])


# Get the negative reviews for movies
neg_tweets = [sanitizer.sanitize(tweet) for tweet
              in twitter_samples.strings('negative_tweets.json')]

# Get the positive reviews for movies
pos_tweets = [sanitizer.sanitize(tweet) for tweet
              in twitter_samples.strings('positive_tweets.json')]

# Find the features that most correspond to negative reviews
negfeats = [(word_feats(f), 'neg') for f in neg_tweets]

# Find the features that most correspond to positive reviews
posfeats = [(word_feats(f), 'pos') for f in pos_tweets]

# We would only use 1500 instances to train on. The quarter of the reviews left is for testing purposes.
negcutoff = int(len(negfeats)*3/4)
poscutoff = int(len(posfeats)*3/4)
