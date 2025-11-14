
def read_file_with_r(file_name):
    with open(file_name, "r") as file:
        f_text = file.read()
        print(f_text)



read_file_with_r("TestDir/data.txt")



