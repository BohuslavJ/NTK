'''
Created by: Bohuslav Juráš
Contact: Bohuslav.juras@seznam.cz
For: NTK
Applying for position: backend developer v python

First task - "Vzdálenost"
This program will calculate distance between two points in 2D array. Points can be either given by name
("Banka, "Lidl" etc.) from enclosed document "mistopis.txt" or by their corresponding position in 2D array ("a1", "c8").
Last option is to give point by any position which is in 2D array range of scope ("a16", "b1"), even if it is not in
"mistopis.txt".
Names are case-sensitive, positions are not.

Functions are written as modules and are being used in other tasks as well. For better readability every task has only
those functions, which are being actively used. If you wish, you can put all tasks and their functions into a single
 .py and nothing of functionality will be lost - on the contrary you can get rid of multiple lines of code this way.
'''

# creation of 2D array - by changing value "size" you can generate and work with differently sized 2D arrays
# if you want to change from which letter/number is matrix starting,
# you can do so by changing values in "rows" and "cols" variables
# this array is actually being used only if you input positions - if you stick to name only, it does not matter
# how large you make this array
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
def vzdalenost(a, b):

    # function which checks if given variable is in 2D matrix even though it is not listed in "mistopis.txt"
    def in_arr_but_not_in_mistopis_check(val):
        for line in arr:
            if val.lower() in line:
                print(f"{val} is not in 'mistopis.txt', but with given coordinate ill calculate it just for you :-*")
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

    # function which decides if value provided by user is name or position in 2D matrix. If it is name, function
    # "get_key" is called. If its position nothing is going happen since we already have what we need. In both cases
    # this function is going to return position in matrix
    def check_array(val):
        if any(val in subl for subl in arr):
            pass
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

    # final function which calculates distance between two positions in 2D matrix. As a first step function
    # "check_correct_input" is called to verify inputs, after that function "split_coordinates" is called and lastly
    # distance will be calculated and returned
    def get_distance(val1, val2):
        val1, val2 = check_correct_input(val1), check_correct_input(val2)
        let1, num1 = split_coordinates(val1)
        let2, num2 = split_coordinates(val2)
        let1, let2 = ord(let1), ord(let2)
        return 20*(abs(let1-let2)+abs(int(num1)-int(num2)))

    return get_distance(a, b)


print(vzdalenost("Lidl", "Banka"))
