def quicksort(arr):
    """Quicksort com pivô mediana-de-três (caso médio robusto)."""
    if len(arr) <= 1:
        return arr
    stack = [(0, len(arr) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        # Mediana de três
        mid = (lo + hi) // 2
        if arr[lo] > arr[mid]:
            arr[lo], arr[mid] = arr[mid], arr[lo]
        if arr[lo] > arr[hi]:
            arr[lo], arr[hi] = arr[hi], arr[lo]
        if arr[mid] > arr[hi]:
            arr[mid], arr[hi] = arr[hi], arr[mid]
        pivot = arr[mid]
        arr[mid], arr[hi - 1] = arr[hi - 1], arr[mid]
        i, j = lo, hi - 1
        while True:
            i += 1
            while arr[i] < pivot:
                i += 1
            j -= 1
            while arr[j] > pivot:
                j -= 1
            if i >= j:
                break
            arr[i], arr[j] = arr[j], arr[i]
        arr[i], arr[hi - 1] = arr[hi - 1], arr[i]
        stack.append((lo, i - 1))
        stack.append((i + 1, hi))
    return arr


def shell_sort(arr):
    """Shell Sort com sequência (1, 4, 10, 23, 57, 132, 301, 701...)."""
    n = len(arr)
    gaps = [1, 4, 10, 23, 57, 132, 301, 701]
    gaps = [g for g in gaps if g < n]
    for gap in reversed(gaps):
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
    return arr
