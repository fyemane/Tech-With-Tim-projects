import numpy as np

print("Given array")
# iterable item (list)
arr = np.array([1, 2, 3])
print(arr)
# not type list, distinct data type
print("Type of array")
print(type(arr))
# outputs dimension of array
print("Shape of array")
print(arr.shape)
# Prints MD array by rows and columns, easier to visualize and calc
print("Difference between normal and numpy array")
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr)
# prints in one flat line
li = [[1, 2, 3], [4, 5, 6]]
print(li)

print("\nIndexing")
# instead of arr[0][1] -> arr[0, 1]
print(arr[0, 1])
print("Shape of array")
print(arr.shape)
# how mnay elements in total
# arrays are typed
print("size of array")
print(arr.size)

print("\nAll array elements are same type")
li = ['jhello', 1, True]
arr = np.array(['jhello', 1, True])
print(arr)

print("\nPrints number of dimensions")
print(arr.ndim)
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr)

print("\nmemory location of data")
print(arr.data)

print("\nAdding elements")
# dot append method doesn't work
# arr[0].append(4)
# array objects are immutable
np.append(arr[0], 99)
print(arr)
arr = np.append(arr, 99)
print(arr)
print("Deleting from arrays")
arr = np.delete(arr, 1)
print(arr)

print("\nCreating arrays")
# prints empty matrix of given dimensions, default float data type
x = np.zeros((2, 3))
print(x)
x = np.zeros((2, 3), dtype=int)
print(x)
x = np.ones((4, 5))
print(x)
x = np.ones((4, 5, 3))
print(x)

print("\nRange function")
x = np.arange(10)
print(x)
x = np.arange(5, 10)
print(x)
x = np.arange(1, 11, 2)
print(x)
x = np.arange(2, 3, 0.1)
print(x)

print("Divides interval by c from a to b")
x = np.linspace(1., 4., 6)
print(x)

print("\nFills array with number")
x = np.full((2, 2), 8)
print(x)

print("Identity matrix")
x = np.eye(5)
print(x)
print("\nCreating random array")
x = np.random.random((4, 5))
print(x)

print("\Matrix operations")
x = np.array([[1, 2], [3, 4]])
y = np.array([[5, 6], [7, 8]])
print(x + y)
print(np.add(x, y))
print(x - y)
print(np.subtract(x, y))
# element wise multiplication
print(x * y)
print(np.multiply(x, y))
print(x / y)
print(np.divide(x, y))
print("square root of elements")
print(np.sqrt(x))

print("\nDot products")
v = np.array([9, 10])
w = np.array([11, 13])
print(v.dot(w))
print(np.dot(v, w))
print("inner product")
print(np.dot(x, y))
print("Transpose matrix")
print(x)
x.T
print(x.T)
h = x.T
print(h)
print(h.T)
print("Sum function")
print(np.sum(x))
# specify axis
# 0 add column, 1 add row
print(np.sum(x, axis=0))
print(np.sum(x, axis=1))