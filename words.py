f = open("words.txt", "r")
words = []
for x in f:
  words += [x[:-1].upper()]
words[-1] += "L"
# print(words)

letter_statuses = {
    "present": [],
    "correct": [],
    "absent": []
}
def filtering_func(word):
    global letter_statuses
    for status in letter_statuses["correct"]:
        if word[status[1]] != status[0]:
            return False
    for status in letter_statuses["present"]:
        if status[0] not in word or word[status[1]] == status[0]:
            return False
    for status in letter_statuses["absent"]:
        if status[0] in word:
            return False
    return True