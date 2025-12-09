from typing import List, Callable, Optional, Any


def linear_search(items: List[Any], predicate: Callable[[Any], bool]) -> Optional[int]:
    for i, it in enumerate(items):
        if predicate(it):
            return i
    return None


def binary_search(sorted_items: List[Any], key_func, value) -> Optional[int]:
    """Assumes sorted_items is sorted by key_func(item). Returns index or None."""
    lo = 0
    hi = len(sorted_items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        k = key_func(sorted_items[mid])
        if k == value:
            return mid
        if k < value:
            lo = mid + 1
        else:
            hi = mid - 1
    return None
