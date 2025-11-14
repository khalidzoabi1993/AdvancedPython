# list of words

word_list = ["apple", "banana", "cherry", "date"]
word_list_1 = ["2", "3", "4", "5"]

# Write words to "words.txt"
def write_words_to_file(file_name, list1):
    with open(file_name, "w") as file:
        for word in list1:
            file.write(word + " " + "\n")


write_words_to_file("words.txt",word_list_1)