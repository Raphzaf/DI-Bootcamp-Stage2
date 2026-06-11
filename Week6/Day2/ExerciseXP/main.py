import numpy as np


# Exercise 1: Array Creation and Manipulation
ex1 = np.arange(10)
print("Exercise 1:")
print(ex1)
print()

# Exercise 2: Type Conversion and Array Operations
ex2_list = [3.14, 2.17, 0, 1, 2]
ex2 = np.array(ex2_list, dtype=int)
print("Exercise 2:")
print(ex2)
print()

# Exercise 3: Working with Multi-Dimensional Arrays
ex3 = np.arange(1, 10).reshape(3, 3)
print("Exercise 3:")
print(ex3)
print()

# Exercise 4: Creating Multi-Dimensional Array with Random Numbers
ex4 = np.random.rand(4, 5)
print("Exercise 4:")
print(np.round(ex4, 2))
print()

# Exercise 5: Indexing Arrays
array_2d = np.array([
    [21, 22, 23, 22, 22],
    [20, 21, 22, 23, 24],
    [21, 22, 23, 22, 22],
])
second_row = array_2d[1]
print("Exercise 5:")
print(second_row)
print()

# Exercise 6: Reversing elements
ex6 = np.arange(10)
reversed_ex6 = ex6[::-1]
print("Exercise 6:")
print(reversed_ex6)
print()

# Exercise 7: Identity Matrix
ex7 = np.eye(4)
print("Exercise 7:")
print(ex7)
print()

# Exercise 8: Simple Aggregate Funcs
ex8 = np.arange(10)
ex8_sum = np.sum(ex8)
ex8_avg = np.mean(ex8)
print("Exercise 8:")
print(f"Sum: {ex8_sum}, Average: {ex8_avg}")
print()

# Exercise 9: Create Array and Change its Structure
ex9 = np.arange(1, 21).reshape(4, 5)
print("Exercise 9:")
print(ex9)
print()

# Exercise 10: Conditional Selection of Values
ex10 = np.arange(10)
odd_numbers = ex10[ex10 % 2 != 0]
print("Exercise 10:")
print(odd_numbers)
