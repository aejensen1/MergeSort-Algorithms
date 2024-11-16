import time
import random
import math
from memory_profiler import memory_usage
import pandas as pd

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

# ------------------------------------------------------------

def measure_mergesort_memory(func, *args):
    def wrapped_function(*wrapped_args):
        func(*wrapped_args)
    return memory_usage((wrapped_function, args), interval=0.01)

# ------------------------------------------------------------

# Chapter 2.2 Mergesort
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

# ------------------------------------------------------------

# Chapter 2.2 Mergesort
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
# Chapter 7.4: Mergesort Revisited
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

    results = []

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

        # Test mergesort1
        start_time = time.time()
        mergesort1(len(S), S)
        time_taken = time.time() - start_time
        memory_used = max(measure_mergesort_memory(mergesort1, len(S), S))
        results.append(["mergesort1", data_type, n, time_taken, memory_used])

        # Test mergesort2
        start_time = time.time()
        mergesort2(0, len(S) - 1, S)
        time_taken = time.time() - start_time
        memory_used = max(measure_mergesort_memory(mergesort2, 0, len(S) - 1, S))
        results.append(["mergesort2", data_type, n, time_taken, memory_used])

        # Test mergesort3
        start_time = time.time()
        mergesort3(len(S), S)
        time_taken = time.time() - start_time
        memory_used = max(measure_mergesort_memory(mergesort3, len(S), S))
        results.append(["mergesort3", data_type, n, time_taken, memory_used])

        # Measure time for mergesort4
        A = [] # Convert the list to a list of Node objects. Not included in time to sort.
        for key in S:
            A.append(Node(key))
        start_time = time.time()
        mergedlist_container = [None]
        mergesort4(0, len(A) - 1, mergedlist_container, A)
        time_taken = time.time() - start_time
        memory_used = max(measure_mergesort_memory(mergesort4, 0, len(A) - 1, mergedlist_container, A))
        results.append(["mergesort4", data_type, n, time_taken, memory_used])

    return results

def prepare_tests():
    # Test for array sizes from 10^1 to 10^6, running 100 tests per size
    num_tests = 2  # Number of tests to run for each array size
    data_types = ['random', 'sorted', 'reversed', 'nearly_sorted']
    results = []

    for x in range(1, 7):  # For array sizes 10^1 to 10^6
        n = 10**x
        print(f"Testing with array size: {n}")

        for data_type in data_types:
            # Run the tests and calculate average times
            test_results = run_tests(num_tests, n, data_type)
            results.extend(test_results)
            print(f"Completed: Data Type={data_type}, Input Size={n}")
                
        # Convert results to a DataFrame
        df = pd.DataFrame(results, columns=["Algorithm", "Data Type", "Input Size", "Time (s)", "Memory (MB)"])

        # Calculate averages
        avg_results = df.groupby(["Algorithm", "Data Type", "Input Size"])[["Time (s)", "Memory (MB)"]].mean().reset_index()

        # Save raw data and averages with unique filenames
        raw_data_file = f"merge_sort_raw_data_{x}.xlsx"
        avg_data_file = f"merge_sort_averages_{x}.xlsx"
        
        with pd.ExcelWriter(raw_data_file) as writer:
            df.to_excel(writer, sheet_name="Raw Data", index=False)

        avg_results.to_excel(avg_data_file, index=False)
        print(f"Results for 10^{x} saved to {raw_data_file} and {avg_data_file}")

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
    print ("Original:", S)

    # Test the mergesort1 function
    print ("Mergesort 1:", mergesort1(len(S), S))

    # Test the mergesort2 function
    print ("Mergesort 2:", mergesort2(0, len(S) - 1, S))

    # Test the mergesort3 function
    print ("Mergesort 3:", mergesort3(len(S), S))

    # Test the mergesort4 function
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