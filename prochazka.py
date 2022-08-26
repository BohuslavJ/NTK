'''
Created by: Bohuslav Juráš
Contact: Bohuslav.juras@seznam.cz
For: NTK
Applying for position: backend developer v python

Fourth task - "prochazka"
This program will print a list of all given inputs, in order in which you are supposed to visit them, to travel the
shortest path possible while starting in first input and ending in second input. Number of inputs is not limited,
but as this is the classical TSP problem solved by bruteforce I would not recommend pushing it too hard. Also, as a
bonus you will also get length of your trip, so that you can flex on your friends with unholy amount of steps you did.

As in previous three tasks, points can be either given by name ("Banka, "Lidl" etc.) from enclosed document
"mistopis.txt" or by their corresponding position in 2D array ("a1", "c8"). Last option is to give point by any position
which is in 2D array range of scope ("a16", "b1"), even if it is not in "mistopis.txt".
'''

# imports of necessary libraries
# pip install python-tsp
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming

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


def vzdalenost(a, b):

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
        let1, num1 = split_coordinates(val1)
        let2, num2 = split_coordinates(val2)
        let1, let2 = ord(let1), ord(let2)
        return 20*(abs(let1-let2)+abs(int(num1)-int(num2)))

    return get_distance(a, b)


# function which calculates path and length of walk with TSP problem
# first block of code is used to calculate all the distances between every two positions in our array
# second block of code is used to create distance matrix out of all the distances we got
# third block of code is used to solve the problem with library and calculate length of the walk
# fourth block of code is used to print out result
def TSP(start, stop, *args):
    places = args
    n = 0
    places = places[: n] + (start,) + places[n:]
    dct = {i: [] for i in places}
    for index, x in enumerate(places):
        index_copy = 0
        while index_copy < len(places):
            dct[x] += [vzdalenost(x, places[index_copy])]
            index_copy += 1

    distance_matrix = []
    for list in dct:
        distance_matrix.append(dct[list])

    distance_matrix = np.array(distance_matrix)
    permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    distance += vzdalenost(start, stop) + vzdalenost(places[permutation[-1]], stop)
    distance -= vzdalenost(places[permutation[0]], places[permutation[-1]])


    for place in permutation:
        print(places[place], end=" ---> ")
    print(stop)
    print(f"you walked {distance}")
    return permutation, distance


TSP("Banka", "Lekarna", "Tesco", "Drogerie", "b4", "Mall", "Globus", "Kaufland", "Penny", "Lidl", "Albert", "AirBank", "Unicredit", "CSOB", "Fio")

