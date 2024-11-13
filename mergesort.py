import time
import random

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


# Function to run the test multiple times and calculate the average time
def run_tests(num_tests, n, data_type):
    mergesort1_times = []
    mergesort2_times = []

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

    # Calculate and return the average time for both mergesorts
    avg_mergesort1_time = sum(mergesort1_times) / num_tests
    avg_mergesort2_time = sum(mergesort2_times) / num_tests
    return avg_mergesort1_time, avg_mergesort2_time

# Test for array sizes from 10^1 to 10^6, running 100 tests per size
num_tests = 3  # Number of tests to run for each array size
data_types = ['random', 'sorted', 'reversed', 'nearly_sorted']

for x in range(1, 7):  # For array sizes 10^1 to 10^6
    n = 10**x
    print(f"Testing with array size: {n}")

    for data_type in data_types:
        # Run the tests and calculate average times
        avg_mergesort1_time, avg_mergesort2_time = run_tests(num_tests, n, data_type)

        # Output the results for each data type
        print(f"Data Type: {data_type}")
        print(f"mergesort1 average time: {avg_mergesort1_time:.6f} seconds")
        print(f"mergesort2 average time: {avg_mergesort2_time:.6f} seconds")
        print("-" * 50)  # Separator for clarity