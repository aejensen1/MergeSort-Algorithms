import time
import random
import math

def generate_random_list(n):
    return [random.randint(1, n) for _ in range(n)]

# Function to generate a sorted list
def generate_sorted_list(n):
    return list(range(1, n + 1))

# Function to generate a reversely sorted list
def generate_reversed_list(n):
    return list(range(n, 0, -1))

# Function to generate a nearly sorted list
def generate_nearly_sorted_list(n, num_swaps=10):
    # Start with a sorted list
    S = list(range(1, n + 1))
    # Swap a few random elements
    for _ in range(num_swaps):
        i, j = random.sample(range(n), 2)
        S[i], S[j] = S[j], S[i]
    return S

def mergesort1(n, S):
    if n > 1:
        h = n // 2
        m = n - h
        
        # Create temporary arrays U and V
        U = [0] * h
        V = [0] * m
        
        # Copy elements to U and V
        for i in range(h):
            U[i] = S[i]
        for i in range(h, n):
            V[i - h] = S[i]
        
        # Recursively sort both halves
        mergesort1(h, U)
        mergesort1(m, V)
        
        # Merge the sorted halves
        merge1(h, m, U, V, S)
    # Return the sorted array
    return S

def merge1(h, m, U, V, S):
    i = j = k = 0  # Initialize indices for U, V, and S
    
    # Merge U and V back into S
    while i < h and j < m:
        if U[i] < V[j]:
            S[k] = U[i]
            i += 1
        else:
            S[k] = V[j]
            j += 1
        k += 1
    
    # If U is exhausted, copy remaining elements of V
    if i >= h:
        for l in range(j, m):
            S[k] = V[l]
            k += 1
    # If V is exhausted, copy remaining elements of U
    else:
        for l in range(i, h):
            S[k] = U[l]
            k += 1

def mergesort2(low, high, S):
    if low < high:
        mid = (low + high) // 2
        mergesort2(low, mid, S)
        mergesort2(mid + 1, high, S)
        merge2(low, mid, high, S)
    return S

def merge2(low, mid, high, S):
    # Create temporary array U to hold the merged section of S
    U = [0] * (high - low + 1)  # Temporary array of size (high - low + 1)
    
    i = low      # Pointer for the left half (S[low:mid])
    j = mid + 1  # Pointer for the right half (S[mid+1:high])
    k = 0        # Pointer for the temporary array U
    
    # Merge elements from both halves into U
    while i <= mid and j <= high:
        if S[i] < S[j]:
            U[k] = S[i]
            i += 1
        else:
            U[k] = S[j]
            j += 1
        k += 1
    
    # Copy any remaining elements from the left half (if any)
    while i <= mid:
        U[k] = S[i]
        i += 1
        k += 1
    
    # Copy any remaining elements from the right half (if any)
    while j <= high:
        U[k] = S[j]
        j += 1
        k += 1

    # Copy the merged array U back to the original array S
    for l in range(low, high + 1):
        S[l] = U[l - low]  # Adjust index by subtracting low

# ------------------------------------------------------------

# Chapter 7.4: Mergesort Revisited
# Mergesort3 (Dynamic Programming Version)
def mergesort3(n, S):
    # Treat array size as a power of 2
    log2_n = math.log2(n)
    ceiling_log2_n = math.ceil(log2_n)
    m = 2 ** ceiling_log2_n  # Next power of 2 >= n

    size = 1  # Size of subarrays being merged (starting from 1)

    # Iterate through the sizes (1, 2, 4, 8, ...)
    for i in range(int(math.log2(m))):  # log2(m) rounds down to an integer
        for low in range(0, m - 2 * size + 1, 2 * size):  # Use zero-based indexing
            mid = low + size - 1
            high = low + 2 * size - 1

            # Ensure high does not exceed n
            if high >= n:
                high = n - 1

            merge3(low, mid, high, S)

        # Double the subarray size for the next pass
        size *= 2
    return S

def merge3(low, mid, high, S):
    # Merge two sorted subarrays S[low..mid] and S[mid+1..high]
    # This function assumes S[low..mid] and S[mid+1..high] are already sorted
    left = S[low:mid+1]   # Subarray from low to mid
    right = S[mid+1:high+1]  # Subarray from mid+1 to high

    i, j, k = 0, 0, low
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            S[k] = left[i]
            i += 1
        else:
            S[k] = right[j]
            j += 1
        k += 1

    # Copy remaining elements from left or right if any
    while i < len(left):
        S[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        S[k] = right[j]
        j += 1
        k += 1

# ------------------------------------------------------------
# Linked Version of Mergesort
class Node:
    def __init__(self, key=None, link=None):
        self.key = key
        self.link = link

def mergesort4(low, high, mergedlist_container, S):
    if low == high:
        # Base case: single node
        mergedlist_container[0] = S[low]
        mergedlist_container[0].link = None
    else:
        mid = math.floor((low + high) / 2)
        
        # Containers for the left and right sorted sublists
        list1_container = [None]
        list2_container = [None]
        
        # Recursively sort the left and right halves
        mergesort4(low, mid, list1_container, S)
        mergesort4(mid + 1, high, list2_container, S)
        
        # Merge the sorted halves and store the result in mergedlist_container
        mergedlist_container[0] = merge4(list1_container[0], list2_container[0])

def merge4(list1, list2):
    # Determine the head of the merged list
    if list1.key < list2.key:
        mergedlist = list1
        list1 = list1.link
    else:
        mergedlist = list2
        list2 = list2.link

    lastsorted = mergedlist
    while list1 is not None and list2 is not None:
        if list1.key < list2.key:
            lastsorted.link = list1
            lastsorted = list1
            list1 = list1.link
        else:
            lastsorted.link = list2
            lastsorted = list2
            list2 = list2.link

    # Attach the remaining nodes from either list1 or list2
    if list1 is None:
        lastsorted.link = list2
    else:
        lastsorted.link = list1

    return mergedlist

# ------------------------------------------------------------
# Function to run the test multiple times and calculate the average time
def run_tests(num_tests, n, data_type):
    mergesort1_times = []
    mergesort2_times = []
    mergesort3_times = []
    mergesort4_times = []

    for _ in range(num_tests):
        # Generate the correct type of list based on data_type
        if data_type == 'random':
            S = generate_random_list(n)
        elif data_type == 'sorted':
            S = generate_sorted_list(n)
        elif data_type == 'reversed':
            S = generate_reversed_list(n)
        elif data_type == 'nearly_sorted':
            S = generate_nearly_sorted_list(n)

        # Test the mergesort1 function
        start_time = time.time()
        mergesort1(len(S), S)
        mergesort1_times.append(time.time() - start_time)

        # Test the mergesort2 function
        start_time = time.time()
        mergesort2(0, len(S) - 1, S)
        mergesort2_times.append(time.time() - start_time)

        # Test the mergesort3 function
        start_time = time.time()
        mergesort3(len(S), S)
        mergesort3_times.append(time.time() - start_time)

        # Test the mergesort4 function
        A = [] # Convert the list to a list of Node objects. Not included in time to sort.
        for key in S:
            A.append(Node(key))
        start_time = time.time()
        mergedlist_container = [None]
        mergesort4(0, len(A) - 1, mergedlist_container, A)
        mergesort4_times.append(time.time() - start_time)

    # Calculate and return the average time for both mergesorts
    avg_mergesort1_time = sum(mergesort1_times) / num_tests
    avg_mergesort2_time = sum(mergesort2_times) / num_tests
    avg_mergesort3_time = sum(mergesort3_times) / num_tests
    avg_mergesort4_time = sum(mergesort4_times) / num_tests
    return avg_mergesort1_time, avg_mergesort2_time, avg_mergesort3_time, avg_mergesort4_time

def prepare_tests():
    # Test for array sizes from 10^1 to 10^6, running 100 tests per size
    num_tests = 2  # Number of tests to run for each array size
    data_types = ['random', 'sorted', 'reversed', 'nearly_sorted']

    for x in range(1, 7):  # For array sizes 10^1 to 10^6
        n = 10**x
        print(f"Testing with array size: {n}")

        for data_type in data_types:
            # Run the tests and calculate average times
            avg_mergesort1_time, avg_mergesort2_time, avg_mergesort3_time, avg_mergesort4_time = run_tests(num_tests, n, data_type)

            # Output the results for each data type
            print(f"Data Type: {data_type}")
            print(f"mergesort1 average time: {avg_mergesort1_time:.6f} seconds")
            print(f"mergesort2 average time: {avg_mergesort2_time:.6f} seconds")
            print(f"mergesort3 average time: {avg_mergesort3_time:.6f} seconds")
            print(f"mergesort4 average time: {avg_mergesort4_time:.6f} seconds")
            print("-" * 50)  # Separator for clarity

# Convert linked list to a Python list (array)
def linked_list_to_array(linked_list):
    array = []
    current = linked_list
    while current is not None:
        array.append(current.key)
        current = current.link
    return array

def test_mergesort():
    S = [10, 3, 7, 4, 8, 5, 2, 9, 6, 1]

    # Test the mergesort1 function
    print ("Mergesort 1:", mergesort1(len(S), S))

    # Test the mergesort2 function
    print ("Mergesort 2:", mergesort2(0, len(S) - 1, S))

    # Test the mergesort3 function
    print ("Mergesort 3:", mergesort3(len(S), S))

    # Test the mergesort4 function
    # S = [Node(10), Node(3), Node(7), Node(4), Node(8), Node(5), Node(2), Node(9), Node(6), Node(1)]
    A = [] # Convert the list to a list of Node objects. Not included in time to sort.
    for key in S:
        A.append(Node(key))
    mergedlist_container = [None]
    mergesort4(0, len(S) - 1, mergedlist_container, A)
    sorted_list_head = mergedlist_container[0]
    print("Mergesort 4:", linked_list_to_array(sorted_list_head))


# Test the implementation
if __name__ == "__main__":
    prepare_tests()
    # test_mergesort()