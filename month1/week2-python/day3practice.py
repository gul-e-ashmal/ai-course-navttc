# WAPto askthe user to enter namesof their 3 favorite movies &store themin alist.
movie_list=[]
movie_list.append(input("Enter your first favorite movie: "))
movie_list.append(input("Enter your second favorite movie: "))
movie_list.append(input("Enter your third favorite movie: "))
print(movie_list)

# WAPto check if alist contains apalindrome of elements. (Hint: use copy( )method)
palindrom=[1,2,3,2,1]
palindrom_cpy=palindrom.copy()
palindrom_cpy.reverse()
if(palindrom==palindrom_cpy):
    print("It is a palindrom")
else:
    print("It is not a palindrom")


# WAPto count the numberof students with the “A” grade in the following tuple.
grade = ("C", "D", "A", "A", "B", "C", "A", "B", "A", "D")         
print(grade.count("A"))

# Store the abovevalues in alist &sort them from “A” to “D”
grade = ["C", "D", "A", "A", "B", "C", "A", "B", "A", "D"]
grade.sort()
print(grade)       
