# Sorting algorithms

def bubble_sort(arr):
	"""
	small data sets
	time complexity: O(n^2) in worst case, O(n) in best case when already sorted
	space complexity: O(1)
	"""
	for i in range(len(arr)):
		for j in range(len(arr) - i):
			temp = None
			if j + 1< len(arr):
				if arr[j] > arr[j + 1]:
					temp = arr[j]
					arr[j] = arr[j + 1]
					arr[j + 1] = temp
	return arr


def insertion_sort(arr):
	"""
	small data sets
	time complexity: O(n^2) worst case, O(n) best case
	space complexity: O(1)
	"""
	for i in range(1, len(arr)):
		value = arr[i]
		j = i - 1
		while j >= 0 and value < arr[j]:
			arr[j + 1] = arr[j]
			j -= 1
		arr[j + 1] = value
	return arr


def selection_sort(arr):
	"""
	small data sets
	time complexity: O(n^2) worst case
	space complexity: O(1) because in-place
	"""
	for i in range(len(arr)):
		min_val = arr[i]
		min_ind = i
		for j in range(i + 1, len(arr)):
			if arr[j] < min_val:
				min_val = arr[j]
				min_ind = j
		arr[min_ind] = arr[i]
		arr[i] = min_val
	return arr

def quick_sort(arr):
	"""
	Good for sorting large unordered data sets with not many duplicates
	time complexity: O(n log n) best case and O(n^2) worst case - already sorted or too many duplicate elements
	space complexity: O(log n) best case and O(n) worst case
	"""
	if len(arr) == 1 or len(arr) == 0:
		return arr
	pivot = arr[-1]
	lhs, rhs = partition(arr, pivot)
	lhs = quick_sort(lhs)
	rhs = quick_sort(rhs)
	return lhs + [pivot] + rhs
	

def partition(arr, pivot):
	lhs = []
	rhs = []
	for i in range(len(arr) - 1):
		if arr[i] <= pivot:
			lhs.append(arr[i])
		else:
			rhs.append(arr[i])
	return lhs, rhs


# need to implement merge sort, radix sort and heap sort
	

print(sort([5, 3, 8, 4, 6]))