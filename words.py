def get_all_words():
    f = open("words.txt", "r")
    words = []
    for x in f:
        words += [x[:-1].upper()]
    print(words)
    words[-1] += str(f)[-1][-1]
    f.close()
    return words

def filtering_func(word, letter_statuses):
    for status in letter_statuses["correct"]:
        if word[status[1]] != status[0]:
            return False
    for status in letter_statuses["present"]:
        if status[0] not in word or word[status[1]] == status[0]:
            return False
    for status in letter_statuses["absent"]:
        if status[0] in word and status[0] not in list(map(lambda x: x[0], letter_statuses["present"]+letter_statuses["correct"])):
            return False
        elif status[0] in word and word[status[1]] == status[0]:
            return False
    return True

def get_count(l, e, c=0):
    for x in l:
        if e == x:
            c += 1
    return c