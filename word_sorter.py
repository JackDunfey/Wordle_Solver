import wordfreq
words = []
with open("alphabetical_words.txt", "r") as f:
    for x in f:
        words += [x[:-1].upper()]
    words[-1] += str(f)[-1][-1]
words.sort(reverse=True, key=lambda word: wordfreq.zipf_frequency(word,"en"))
with open("words.txt", "w") as p:
    p.write("\n".join(words))