# A program to clean, sort, and search a list of numbers!
APP_NAME = """Mini Number Helper"""


def clean_input(user_input: str) -> list[int] | None:
    """This function return the list of integers only from user's input comma sepearted numbers"""
    cleaned_list = []
    tokens = user_input.split(",")

    for token in tokens:
        try:
            number = int(token.strip())
            cleaned_list.append(number)
        except ValueError:
            continue

    return cleaned_list or None


def selection_sort(numbers: list[int]) -> list[int]:
    """Return a new list sorted in ascending order using selection sort."""
    array = numbers[:]  # copy
    n = len(array)
    indexing_length = range(n - 1)

    for i in indexing_length:
        min_value = i

        for j in range(i + 1, n):
            if array[j] < array[min_value]:
                min_value = j

        if min_value != i:
            array[min_value], array[i] = array[i], array[min_value]

    return array


def linear_search(array: list[int], target: int) -> int:
    """Return index of target in array using linear search, or -1 if not found."""
    indexes = []
    for i in range(len(array)):
        if array[i] == target:
            indexes.append(i)

    return indexes if indexes else -1  # type: ignore


def format_indexes(indexes: list[int]) -> str:
    """This function turn indexes into human readable foramt For e.g. "2" or "2 and 3" or  "2, 3 and 4" """
    indexes = list(map(str, indexes))  # type: ignore

    if len(indexes) <= 2:
        return " and ".join(indexes)  # type: ignore
    return ", ".join(indexes[:-1]) + " and {indexes[-1]}"  # type: ignore


def run_tests():
    print("====== Ruuning Tests ======")

    # Test 1: selection sort
    test_list = [4, 9, 7, 8, 0, 2, 1, 3, 6, 5, 2]
    expected_sort = [0, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9]

    assert selection_sort(test_list) == expected_sort
    assert test_list == [4, 9, 7, 8, 0, 2, 1, 3, 6, 5, 2]

    # Test 2: Linear Search
    assert linear_search(test_list, 2) == [5, 10]
    assert linear_search(test_list, 99) == -1

    # Test 3 - Cleaned number in list
    user_numbers = "6, apple, 7, orange, 10, 6"
    cleaned_number = [6, 7, 10, 6]
    assert clean_input(user_numbers) == cleaned_number

    print("All test passed!")


def main():
    print(f"----- Welcome to {APP_NAME} -----\n")
    run_tests()
    print("-" * 40)

    # Input loop
    while True:
        user_input = input("Enter numbers seperated by commas:\n")
        number_lists = clean_input(user_input)

        if number_lists is not None:
            break

        print("\nError: No valid numbers entered. Please try again.\n")

    print(f"\nOriginal list: {number_lists}")
    sorted_list = selection_sort(number_lists)  # type: ignore
    print(f"Sorted list: {sorted_list}")

    # Search loop
    while True:
        choice = input("\nEnter a number to search for (or 'q' to quit search):")
        if choice.lower().strip() == "q":
            break

        try:
            target_num = int(choice)
        except ValueError:
            print("Invalid number. Try again.")
            continue

        index = linear_search(sorted_list, target_num)

        if index != -1:
            formatted = format_indexes(index)  # type: ignore
            print(f"Found {target_num} at index {formatted} in the sorted list.")
        else:
            print(f"{target_num} not found in the list")

    print(f"----Thank you for using {APP_NAME}----")


if __name__ == "__main__":
    main()
