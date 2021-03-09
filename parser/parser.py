import nltk
import sys
import re
import string

SENTENCES = ["the home had a mess", "his smile lit my home", "thursday arrived before holmes",
             "a red little country home", "I smile", "she chuckled at the mess",
             "we left in a hurry", "we said a word", "the armchair is red",
             "I had a walk to my home", "we walk on a country", "palm before a lit pipe smiled",
             "armchair said at a pipe", "I had a moist palm", "we smiled and she never",
             "his companion never arrived", "we were here until she came",
             "I arrived in the country", "my until the day came here",
             "an armchair said to a companion"]

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | NP VP Conj VP
AP -> Adj | Adj AP
NP -> N | Det NP | AP NP | NP PP
PP -> P NP | P S
VP -> V | V NP | V NP PP | V PP | VP Adv | Adv VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    if len(s) is 0:
        for sentence in SENTENCES:
            print("PARSING SENTENCE: "+sentence)
            parse(sentence)
            print("")
            print("")

    else:
        parse(s)


def parse(s):
    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks (" + str(len(np_chunk(tree))) + ")")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    pattern = re.compile('[%s]' % re.escape(string.punctuation))
    sentence_clean = pattern.sub('', sentence)
    sentence_clean = re.sub('\d', '', sentence_clean)
    tokenized = nltk.word_tokenize(sentence_clean.lower())

    return tokenized


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    for s in tree.subtrees(lambda t: t.height() == 3):
        if s.label() == "NP":
            chunks.append(s)

    return chunks


if __name__ == "__main__":
    main()
