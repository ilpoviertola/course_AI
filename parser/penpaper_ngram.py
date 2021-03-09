import re


def read(file):
    content = []
    stopwords = ["a", "an", "and", "as", "at", "for", "from", "in", "into", "of", "on", "or", "the", "to"]
    delimiters = " ", ", ", ",", "'", "\"", ".", ". ", "(", ")", "-", ":", ";", "!", "?"
    regex = '|'.join(map(re.escape, delimiters))

    inp = open(file, "r")
    tmp = inp.read().splitlines()
    for row in tmp:
        for word in re.split(regex, row):
            word = word.lower()
            if len(word) >= 2 and word not in stopwords and not word.isnumeric():
                content.append(word)

    print("File read.")
    return content


def create_bigram_with_probabilities(data):
    bigrams = {}
    zip_list = list(zip(data[0:], data[1:]))

    for bigram in zip_list:
        if bigram not in bigrams:
            divider = 0
            for b in zip_list:
                if bigram[0] is b[0]:
                    divider += 1

            bigrams[bigram] = float(zip_list.count(bigram) /
                                    divider)

    count = sum(bigrams.values())
    for bg in bigrams:
        bigrams[bg] = bigrams[bg] / count

    return bigrams


def main():
    data = read("/Users/ilpoviertola/Code4School/AI/parser/penpaperfile.txt")
    bigrams = create_bigram_with_probabilities(data)
    s = ("blue", "sky")

    if s in bigrams.keys():
        print("Probability of "+str(s)+": "+str(bigrams[s]))
    else:
        print(":(")


if __name__ == '__main__':
    main()