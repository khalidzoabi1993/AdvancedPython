# Program with an error
student_grades = {"Alice": 95, "Bob": 88, "Charlie": 75, "David": 92}


# print(student_grades.get("AlicE", "Not Exist"))
# Attempt to access Sarah's grade
# sarah_grade = student_grades["Sarah", "Not Exist"]

# print(f"Sarah's grade is: {sarah_grade}")

# for i in student_grades:
#     print(f"{i}: {student_grades[i]}")

# print only keys
# print(student_grades.keys())
for key in student_grades.keys():
    if key == "Bob":
        print(f"Key: {key}")

# add to dictionary
student_grades["Eve"] = 89
##############################################
# Program with an error
# courses = {
#     "Math": {"students": ["Alice", "Bob", "Charlie"], "teacher": "Ms. Johnson"},
#     "Science": {"students": ["Alice", "David", "Eve"], "teacher": "Mr. Smith"},
#     "History": {"students": ["Charlie", "David", "Frank"], "teacher": "Mrs. Davis"},
# }
#
# # Attempt to access the students in the 'English' course
# # english_students = courses["English"]["students"]
# # english_students = courses["English"]["students"]
# math_students = courses["Math"]["students"]
# print(math_students[1])
# print(f"Math course students: {math_students}")
