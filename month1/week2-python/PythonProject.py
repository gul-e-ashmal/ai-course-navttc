print("SCHOOL MANAGEMENT SYSTEM")

subjects=["English","Urdu","Maths","Science"]
student_record={'1':{"Name": "A", 
                    "Age": "12", 
                    "Address": "Lahore",
                    "Class": "1", 
                    "Marks": [("English", 90), ("Urdu", 80), ("Maths", 70), ("Science", 60)]},
                    
                '2':{"Name": "B", 
                    "Age": "19", 
                    "Address": "Islamabad",
                    "Class": "1", 
                    "Marks": [("English", 80), ("Urdu", 80), ("Maths", 65), ("Science", 60)]}}

flag=True

# add  new student
def add_student(): 
    name=input("Enter the student name: ")
    age=input("Enter the student age: ")
    address=input("Enter the student address: ")
    classes=int(input("Enter the student class: "))
    marks=[]

    for subject in subjects:
        mark=int(input(f"Enter the marks of {subject}: "))
        marks.append((subject,mark))
    
    student_id=str(len(student_record)+1)
    student_record[student_id] = {"Name": name, "Age": age, "Address": address, "Class": classes, "Marks": marks}
    print(student_record)


#  display  all student
def display_student():
    # print(student_record)
    for student in student_record:
        print(student_record[student],'\n')


# search  student by id
def search_student():
     student_id=input("Enter the student id: ")
     if student_id in student_record:
         print(student_record[student_id])
     else:
         print("Record not found")

def update_student():
    student_id=input("Enter the student id: ")
    if   student_id in student_record:
        name=input("Enter the student name: ")
        age=input("Enter the student age: ")
        address=input("Enter the student address: ")
        classes=int(input("Enter the student class: "))
        marks=[]

        for subject in subjects:
            mark=int(input(f"Enter the marks of {subject}: "))
            marks.append((subject,mark))
        student_record[student_id] = {"Name": name, "Age": age, "Address": address, "Class": classes, "Marks": marks}
        print(student_record)
    else:
        print("Record not found")


def delete_student():
    student_id=input("Enter the student id: ")
    if student_id in student_record:
        print(student_record.pop(student_id, "Not Found"))
        # del student_record[student_id]
        print("Record deleted")
    else:
        print("Record not found")



while flag :
    operation=input("Enter the operation:\n1.Add\n2.Display\n3.Search\n4.Modify\n5.Delete\n6.Exit\n")
    if operation=='1':
        add_student()
    elif operation=='2':
        display_student()
    elif operation=='3':
        search_student()
    elif operation=='4':
        update_student()
    elif operation=='5':
        delete_student()
    else:
        flag=False