# IMPORTS
import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup as bs
from collections import defaultdict
from math import log

# VARIABLES
htmltags = [
    "title", "p", "h1", "h2", "h3", "h4", "h5", "h6", "strong", "em", "li", "td", "th"
]
punctuation_table = {
    ord("!"): None, ord("'"): None, ord(","): None, ord("-"): None, ord("."): None, 
    ord(":"): None, ord(";"): None, ord("?"): None, ord("_"): None, ord("`"): None
}

# HELPERS FUNCTIONS
def alphanumeric_check(char: str) -> bool:
    """
    Checks whether or not the char is an alphanumeric character. Used in the tokenizer function.
    """
    an = "abcdefghijklmnopqrstuvwxyz1234567890"
    if char.lower() not in an:
        return False
    return True

def check_vowel_2nd_last_index(text: str) -> bool:
    """
    Takes in a string of text and checks if there is any vowel before the second last index. Returns True if 
    found, otherwise False.
    """
    return (("a" in (text[0:len(text) - 2])) or ("i" in (text[0:len(text) - 2])) or ("u" in (text[0:len(text) - 2])) 
            or ("e" in (text[0:len(text) - 2])) or ("o" in (text[0:len(text) - 2])))

def check_vowel_3rd_last_index(text: str) -> bool:
    """
    Takes in a string of text and checks if there is any vowel before the third last index. Returns True if 
    found, otherwise False.
    """
    return (("a" in (text[0:len(text) - 3])) or ("i" in (text[0:len(text) - 3])) or ("u" in (text[0:len(text) - 3])) 
            or ("e" in (text[0:len(text) - 3])) or ("o" in (text[0:len(text) - 3])))

def check_vowel_4th_last_index(text: str) -> bool:
    """
    Takes in a string of text and checks if there is any vowel before the fourth last index. Returns True if 
    found, otherwise False.
    """
    return (("a" in (text[0:len(text) - 4])) or ("i" in (text[0:len(text) - 4])) or ("u" in (text[0:len(text) - 4])) 
            or ("e" in (text[0:len(text) - 4])) or ("o" in (text[0:len(text) - 4])))

def check_vowel_5th_last_index(text: str) -> bool:
    """
    Takes in a string of text and checks if there is any vowel before the fifth last index. Returns True if 
    found, otherwise False.
    """
    return (("a" in (text[0:len(text) - 5])) or ("i" in (text[0:len(text) - 5])) or ("u" in (text[0:len(text) - 5])) 
            or ("e" in (text[0:len(text) - 5])) or ("o" in (text[0:len(text) - 5])))

def adjust_stem(text: str) -> str:
    """
    Takes in a string of text and adjusts the current text to make it a stem. Returns the string as a stem. No changes
    are made if the following conditions are not met.
    """
    new_stem = text
    if new_stem.endswith("at") or new_stem.endswith("bl") or new_stem.endswith("iz"):
        new_stem += "e"
    elif ((len(new_stem) >= 2) and (not new_stem.endswith("ll") or new_stem.endswith("ss") or new_stem.endswith("zz")) and 
            new_stem[-1] == new_stem[-2]):
        new_stem = new_stem.removesuffix(new_stem[-1])
    elif (len(new_stem) <= 3):
        new_stem += "e"
    return new_stem

def porter_stemmer(text: str) -> str:
    """
    Takes in a string of text and uses porter stemming in order to remove any suffixes. Returns the string 
    as a stem. It will not parse words if there are no suffixes.
    """
    new_word = text
    # step 1a:
    if (len(new_word) >= 4) and new_word.endswith("sses"):
        new_word = new_word.removesuffix("sses")
        new_word += "ss"
    if ((len(new_word) > 2) and new_word.endswith("s") and new_word[-2] != "s" and new_word[-2] != "u" and 
            check_vowel_2nd_last_index(new_word) and (not (("a" in (new_word[-2])) or ("i" in (new_word[-2])) or 
                                                           ("u" in (new_word[-2])) or ("e" in (new_word[-2])) or 
                                                           ("o" in (new_word[-2]))))):
        new_word = new_word.removesuffix("s")
    if (len(new_word) >= 3) and new_word.endswith("ied") or new_word.endswith("ies"):
        if len(new_word.removesuffix(new_word[-3:])) > 1:
            new_word = new_word.removesuffix(new_word[-3:])
            new_word += "i"
        else:
            new_word = new_word.removesuffix(new_word[-3:])
            new_word += "ie"
    # step 1b:
    if ((len(new_word) > 3) and new_word.endswith("eed") and (new_word[-4] != "a" or new_word[-4] != "i" or 
        new_word[-4] != "u" or new_word[-4] != "e" or new_word[-4] != "o") and check_vowel_3rd_last_index(new_word)):
        new_word = new_word.removesuffix("eed")
        new_word += "ee"
        return new_word
    elif ((len(new_word) > 5) and new_word.endswith("eedly") and (new_word[-6] != "a" or new_word[-6] != "i" or 
          new_word[-6] != "u" or new_word[-6] != "e" or new_word[-6] != "o") and check_vowel_5th_last_index(new_word)):
        new_word = new_word.removesuffix("eedly")
        new_word += "ee"
        return new_word
    if ((len(new_word) > 2) and new_word.endswith("ed") and new_word[-3] != "e" and check_vowel_2nd_last_index(new_word)):
        new_word = new_word.removesuffix("ed")
        new_word = adjust_stem(new_word)
    elif ((len(new_word) > 3) and new_word.endswith("ing") and check_vowel_3rd_last_index(new_word)):
        new_word = new_word.removesuffix("ing")
        new_word = adjust_stem(new_word)
    elif ((len(new_word) > 4) and new_word.endswith("edly") and check_vowel_4th_last_index(new_word)):
        new_word = new_word.removesuffix("edly")
        new_word = adjust_stem(new_word)
    elif ((len(new_word) > 4) and new_word.endswith("ingly") and check_vowel_5th_last_index(new_word)):
        new_word = new_word.removesuffix("ingly")
        new_word = adjust_stem(new_word)

    return new_word

def defrag_url(url: str) -> str:
    """
    Given a url as a string, it returns that url without its fragments.
    """
    parsed_url = urlparse(url)
    defragged_url = urlunparse(parsed_url._replace(fragment=""))
    return defragged_url

def tfidf(freq: int, docfreq: int, docnum: int) -> float:
    """
    Weight formula for TF-IDF:
    w(x,y) = (1 + log(tf(x,y))) * log(N/df(x))
        - log is base 10
        - tf(x,y) = freq of x in y
        - df(x) = # of documents containing x
        - N = total # of documents
    """
    n = docnum
    if freq > 0:
        tf = 1 + log(freq, 10)
    else:
        tf = 0
    idf = log((n/docfreq), 10)
    return round(tf * idf, 2)

def extract_tokenize_fields(jsondict: dict) -> defaultdict:
    """
    An updated version tokenizer that also extracts text. This tokenizer will also record the fields of each token.

    Data in the dictionary(k:v):
        token <str> : [freq <int>, {field <str>, ..., n} <set>]<list>
    """
    tokens = defaultdict(list)
    html = bs(str(jsondict["content"]), "html.parser")
    for e in html.find_all(htmltags):
        tag = e.name
        text = (e.get_text()).replace("\\t"," ").replace("\\n"," ").replace("\\x"," ").replace("\\d"," ").replace("\\r"," ")
        words = text.split()
        for word in words:
            word = word.translate(punctuation_table)
            if not is_valid_token(word):
                continue
            word = word.lower()
            word = porter_stemmer(word)
            if len(tokens[word]) == 0:
                tokens[word].append(1)
                tokens[word].append(set())
                tokens[word][1].add(tag)
            else:
                tokens[word][0] += 1
                tokens[word][1].add(tag)
    return tokens

def is_valid_token(token: str) -> bool:
    """
    Checks whether the string provided is a valid token:
        - is alphanumeric_check
        - 
    """
    if len(token) < 3:
        return False
    for char in token:
        if alphanumeric_check(char):
            continue
        else:
            return False
    return True
