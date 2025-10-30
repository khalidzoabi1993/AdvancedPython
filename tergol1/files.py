# Write a Python program to read an entire text file.
def read_file(file_name):
    with open(file_name) as file:
        print(file.read())


print("read_file: ")
print(read_file("files/read_file.txt"))
print("*****************************************************")


#  Write a Python program to read a file line by line store it into an array.
def read_file_line_by_line(file_name):
    content_array = []
    with open(file_name) as f:
        # content_array is the list that contains the read lines.
        for line in f:
            content_array.append(line)
            print(content_array)


print("read_file_line_by_line: ")
print(read_file_line_by_line("files/read_file_line_by_line.txt"))
print("*****************************************************")


# Write a Python program to write a list content to a file.
def list_to_file(l):
    with open("files/list_to_file.txt", "w") as myfile:
        for c in l:
            myfile.write("%s\n" % c)

    content = open("files/list_to_file.txt")
    print(content.read())


print("list_to_file: ")
color = ["Red", "Green", "White", "Black", "Pink", "Yellow"]
random_list = ["a", "b", "c", "d", "e", "f"]
print(list_to_file(random_list))
print(list_to_file(color))
print("*****************************************************")


# Write a Python program to copy the contents of a file to another file
def copy_file(file_name):
    with open(file_name) as f:
        with open("files/copy_file_b.txt", "w") as f1:
            for line in f:
                f1.write(line)

    content = open("files/copy_file_b.txt")
    print(content.read())


print("copy_file: ")
print(copy_file("files/copy_file_a.txt"))
print("*****************************************************")


# write copy_file with using "w" mode
def copy_file_w(file_name):
    with open(file_name) as f:
        with open("files/copy_file_w.txt", "w") as f1:
            f1.write(f.read())

    content = open("files/copy_file_w.txt")
    print(content.read())


# write a Python program to check if two files are identical.
def check_identical(file_name1, file_name2):
    with open(file_name1) as f1:
        with open(file_name2) as f2:
            if f1.read() == f2.read():
                return True
            else:
                return False


print("check_identical: ")
print(check_identical("files/check_identical_1.txt", "files/check_identical_2.txt"))
print("*****************************************************")


# Write a program that reads a text file and prints the number of occurrences of each word
def word_count(file_name):
    with open(file_name) as f:
        count = {}
        for line in f:
            words = line.split()
            for word in words:
                if word not in count:
                    count[word] = 1
                else:
                    count[word] += 1
        return count


print("word_count: ")
print(word_count("files/word_count.txt"))
print("*****************************************************")
