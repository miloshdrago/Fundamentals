#!/usr/bin/env python3

# dependencies
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


# test dependencies
import unittest

class SanitizerTestCase(unittest.TestCase):
    """
    Class as a testcase for the Sanitizer class.
    """

    def test_remove_punctuation(self):
        text = "remove this: and any other comma's ,"
        equals = "remove this and any other commas"
        sanitizer = Sanitizer()
        self.assertEqual(sanitizer.remove_punctuation(text), equals)

    def test_remove_stopwords(self):
        text = "in the building where an animal lives"
        equals = "building animal lives"
        sanitizer = Sanitizer()
        self.assertEqual(sanitizer.remove_stopwords(text), equals)

    def test_remove_links(self):
        texts = [
            "i contain a link to http://www.google.com",
            "i contain a link to https://www.google.com",
            "i contain a link to www.google.com",
            "i contain a link to www.google.nl",
        ]
        equals = "i contain a link to"
        sanitizer = Sanitizer()
        for text in texts:
            self.assertEqual(sanitizer.remove_links(text), equals)

    def test_remove_usertags(self):
        texts = [
            "i contain a @usertag",
            "i contain a @usertag @anotherusertag",
            "i contain a @usertag @another @usertagTag",
            "@usertag i contain a"
        ]
        equals = "i contain a"
        sanitizer = Sanitizer()
        for text in texts:
            self.assertEqual(sanitizer.remove_usertags(text), equals)

    def test_remove_hashtags(self):
        texts = [
            "i contain a #hashtag",
            "i contain a #hastags #anotherhashtags",
            "i contain a #HasHtags #another#hashtag",
            "#hashag i contain a"
        ]
        equals = "i contain a"
        sanitizer = Sanitizer()
        for text in texts:
            self.assertEqual(sanitizer.remove_hashtags(text), equals)

    def test_lemmatize_words(self):
        text = "animals that are running and laughing"
        equals = "animal that are running and laughing"
        sanitizer = Sanitizer()
        self.assertEqual(sanitizer.lemmatize(text), equals)


    def test_tokenize_words(self):
        text = "split these words . up in 'tokens'"
        equals = ["split", "these", "words", ".", "up", "in", "'", "tokens", "'"]
        sanitizer = Sanitizer()
        self.assertEqual(sanitizer.tokenize(text), equals)

    def test_sanitize(self):
        text = "split . animals into @myuser #test n"
        equals = ["split", "animal"]
        sanitizer = Sanitizer()
        self.assertEqual(sanitizer.sanitize(text), equals)

# run tests as main
if __name__ == "__main__":
    unittest.main()
