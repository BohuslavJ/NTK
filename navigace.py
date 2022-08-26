'''
Created by: Bohuslav Juráš
Contact: Bohuslav.juras@seznam.cz
For: NTK
Applying for position: backend developer v python

Third task - "Navigace"
This program will print all possible shortest paths from one position in 2D matrix to the second position.

As in previous two tasks, points can be either given by name ("Banka, "Lidl" etc.) from enclosed document "mistopis.txt"
or by their corresponding position in 2D array ("a1", "c8"). Last option is to give point by any position which is in 2D
array range of scope ("a16", "b1"), even if it is not in "mistopis.txt".

!!!
Known issue during bug testing - higher value can NOT be put as a first input before lower value!!! Will be fixed in
later version (as I am typing this it is 23:56, and I want go to sleep :D)
!!!

'''

# creation of 2D array - by changing value "size" you can generate and work with differently sized 2D arrays
# if you want to change from which letter/number is matrix starting,
# you can do so by changing values in "rows" and "cols" variables
size = 16
rows, cols = list(map(chr, range(97, 97+size))), list(range(1, 1+size))

# creation of zero matrix with dimensions - size * size
arr = [[0 for x in range(size)] for y in range(size)]

# filling of zero matrix with positions. Lines are marked with ascii letters and columns are marked with numerals.
for row in range(size):
    for col in range(size):
        arr[row][col] = str(rows[row]) + str(cols[col])


# this opens "mistopis.txt", reads and saves values and closes document after
# because of this each name in "mistopis.txt" will have its specific position in matrix
# if you want to add any, simple add them to "mistopis.txt"
file = open("mistopis.txt", 'r')
data_dict = {}
for line in file:
    k, v = line.strip().split()
    data_dict[k.strip()] = v.strip()
file.close()


# main function which will be called
def navigace(val1, val2):

    # function which checks if given variable is in 2D matrix even though it is not listed in "mistopis.txt"
    def in_arr_but_not_in_mistopis_check(val):
        for line in arr:
            if val.lower() in line:
                print(f"{val} is not in 'mistopis.txt', but I will show you show you path to this position")
                return val, True
        return val, False

    # function which checks if given variable is in "mistopis.txt". If it is not, it will call function
    # "in_arr_but_not_in_mistopis_check", to find out, if this variable is at least in 2D matrix. If neither is true,
    # user will be asked to provide new variable. After failing to provide suitable variable five times process will end
    # automatically.
    def check_correct_input(x):
        counter = 0
        while x not in data_dict.keys() and x not in data_dict.values():
            x, decision = in_arr_but_not_in_mistopis_check(x)
            if decision == True:
                return x.lower()
            if counter == 5:
                print("terminating process - go read what you are supposed to input and try again")
                exit()
            else:
                x = input(f"you miss clicked for sure because {x} is not in 'mistopis.txt' - kindly give me new value ---> ")
                counter += 1
        return x

    # function which gives position to name, from "mistopis.txt", if user opted to use name as an input variable and
    # returns this position
    def get_key(val):
        for key, value in data_dict.items():
            if val == value:
                return key

    # function which gives name to position, from "mistopis.txt", if user opted to use position as an input variable and
    # returns this name
    def get_value(val):
        for key, value in data_dict.items():
            if val == key:
                return value

    # function which decides if value provided by user is name or position in 2D matrix. If it is name, function
    # "get_key" is called. If its position function "get_value" is called. After this function is done we will have both
    # position and name of input
    def check_array(val):
        if any(val in subl for subl in arr):
            global var
            var = get_value(val)
        else:
            val = get_key(val)
        return val

    # function which splits position in 2D matrix into ascii and numerical part, which will be used for final
    # calculation of distance. As a first step, this function will call function "check_array" to change input variable
    # into position in 2D matrix. This position will be returned as 2 parts.
    def split_coordinates(val):
        val = check_array(val)
        numerals, letters = "", ""
        for letter in val:
            if letter.isdigit():
                numerals += letter
            else:
                letters += letter
        return letters, numerals

    # function which will create 2D matrix starting from "val1" position in top left
    # to end with "val2" position in bottom right. Also returns the size of matrix - height and length

    # in first block of code previous functions are called to check validity of inputs with "check_correct_input" and
    # after that "check_array" function is called as an argument of "split_coordinates" function to get our starting
    # row and column as well as our end row and column

    # second block of code is used to make 2 lists - one with all the ascii symbols starting from "val1" to "val2"
    # and another list with all the numbers starting from "val1" to "val2". After that we extract length on these
    # two lists, which will give us the final dimensions for our new matrix

    # finally, last (third) block of code is used to create 2D matrix "mat" and populate it with corresponding values
    # height of "mat" will be "high_of_mat", length will be "length_of_mat" and values will be taken from "rows" and
    # "cols" respectively
    def create_2D_matrix(val1, val2):
        val1, val2 = check_correct_input(val1), check_correct_input(val2)
        x1, y1 = (split_coordinates(check_array(val1)))
        x2, y2 = (split_coordinates(check_array(val2)))

        rows = list(map(chr, range(ord(x1), ord(x2) + 1)))
        cols = list(range(int(y1), int(y2) + 1))
        high_of_mat, length_of_mat = len(rows), len(cols)

        mat = [[0 for x in range(len(cols))] for y in range(len(rows))]
        for row in range(len(rows)):
            for col in range(len(cols)):
                mat[row][col] = str(rows[row]) + str(cols[col])
        return mat, high_of_mat, length_of_mat

    # calling of "create_2D_matrix" function to get all necessary data before last step
    mat, high_of_mat, len_of_mat = create_2D_matrix(val1, val2)

    # recursive function which will go through all different paths and print results
    def print_all_paths(mat, i, j, high, len, path, pi):

        # reached the bottom of the matrix, so we are left with only option to move right
        if i == high - 1:
            for k in range(j, len):
                path[pi + k - j] = mat[i][k]
            for l in range(pi + len - j):
                print(path[l], end=" ")
            print()
            return

        # reached the right corner of the matrix, we are left with only the downward movement
        if j == len - 1:
            for k in range(i, high):
                path[pi + k - i] = mat[k][j]
            for l in range(pi + high - i):
                print(path[l], end=" ")
            print()
            return

        # add the current cell to the path being generated
        path[pi] = mat[i][j]

        # first call of function is for moving down - prints all the paths that are possible after moving down
        # second call of function is for moving right - prints all the paths that are possible after moving right
        print_all_paths(mat, i + 1, j, high, len, path, pi + 1)
        print_all_paths(mat, i, j + 1, high, len, path, pi + 1)

    # the main function that calls function "print_all_paths" to print all possible paths from top left to bottom right
    # in a matrix 'mat' of size "high_of_mat"*"len_of_mat"
    def why_are_we_still_here_just_to_suffer(mat, high_of_mat, len_of_mat):
        path = [0 for i in range(high_of_mat + len_of_mat)]
        print_all_paths(mat, 0, 0, high_of_mat, len_of_mat, path, 0)

    # final call of function with the information we gathered previously from user input and our built functions
    # yes I am aware of the name - it was placeholder at first, but considering how long it took me to built I am
    # keeping that name as a tribute
    why_are_we_still_here_just_to_suffer(mat, high_of_mat, len_of_mat)

navigace("a2", "F6")