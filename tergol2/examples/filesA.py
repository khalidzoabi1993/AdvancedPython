# Additional list of words to append
aditional_words = ["fig", "grape", "kiwi", "lemon"]
# Append new words to "words.txt"
with open("words.txt", "a") as file:
    for word in aditional_words:
        file.write(word + "\n")