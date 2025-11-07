# list of words

word_list = ["apple", "banana", "cherry", "date"]

# Write words to "words.txt"

with open("words.txt", "w") as file:
    for word in word_list:
        file.write(word + " ")

# apple banana cherry date