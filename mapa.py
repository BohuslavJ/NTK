'''
Created by: Bohuslav Juráš
Contact: Bohuslav.juras@seznam.cz
For: NTK
Applying for position: backend developer v python

Second task - "Mapa"
This program will print a "map" of all given inputs according to their position in document "mistopis.txt".
As in previous task, points can be either given by name ("Banka, "Lidl" etc.) from enclosed document "mistopis.txt" or
by their corresponding position in 2D array ("a1", "c8"). Last option is to give point by any position which is in 2D
array range of scope ("a16", "b1"), even if it is not in "mistopis.txt".
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
def mapa(*args):

    # function which checks if given variable is in 2D matrix even though it is not listed in "mistopis.txt"
    def in_arr_but_not_in_mistopis_check(val):
        for line in arr:
            if val.lower() in line:
                print(f"{val} is not in 'mistopis.txt', but I will mark it on map for you as U (Undefined)")
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

    # creating of list that has positions in 2D matrix of all args that user provided
    list = []
    for name in args:
        name = check_correct_input(name)
        list.append(check_array(name))

    # final function of "Mapa" program, which is responsible for final print out of map.
    # First function takes our already created 2D matrix ("arr") and starts looping through all rows and all columns.
    # Whenever position which is in "list" is reached instead of "+" - which signalize, that this position is empty,
    # first letter of name corresponding to this position is printed ("a1":"Banka" is gonna print "B"). If there is no
    # corresponding name to position in "list" function will print "U" standing for "Undefined" instead.

    # part of empty map will look like this:

    #  +---+---+
    #  |   |   |
    #  +---+---+
    #  |   |   |
    #  +---+---+

    # "+" are positions where name shortcut can be placed
    # other symbols ("---" and "|") are just spacing to make map look good


    def generate_map(arr):
        for index1, map_row in enumerate(arr):
            for index, map_col in enumerate(map_row):
                if map_col in list:
                    try:
                        first_char = str(data_dict[map_col])[0]
                        print(first_char, end="")
                    except KeyError:
                        print("U", end="")
                    except:
                        first_char = var[0]
                        print(first_char, end="")
                else:
                    print("+", end="")
                if index != size - 1:
                    print("---", end="")
            print()
            if index1 != size - 1:
                for x in range(size):
                    print("|", end="   ")
            print()

    generate_map(arr)


mapa("Bank", "Lekarn", "Drogerie", "Tesco", "b3", "Mall", "Globus", "Kaufland", "Penny", "Lidl", "Albert",
     "AirBank", "Unicredit", "CSOB", "Fio", "L3", "k12")
