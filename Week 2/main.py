def parse_items(raw: str, ignore_list: set[str]) -> list[str]:
    words = raw.lower().replace(",", " ").split()
    filtered = [w for w in words if w not in ignore_list]
    return filtered


def count_items(items: list[str]) -> dict[str, int]:
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


def top_n(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:n]


def main():
    print("Enter your shopping list (comma-seperated):")

    shopping_items = []
    while True:
        all_items = input(">").strip()
        if all_items == "":
            break
        shopping_items.append(all_items)

    raw_input_line = (", ").join(shopping_items)

    ignore_words = {"a", "and", "the"}
    items = parse_items(raw_input_line, ignore_words)
    counts = count_items(items)

    total_items = len(items)
    unique_items = len(counts)

    print("\n=== Shopping List Summary ===")
    print(f"Total items entered: {total_items}")
    print(f"Number of unique items: {unique_items}")

    print("\nItem Frequency Table:")
    for item, count in counts.items():
        print(f"{item}: {count}")

    while True:
        try:
            n = int(input("\nHow many top frequent items to show? "))
            if n <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive integer.\n")

    print(f"\nTop {n} most frequent items:")
    for item, count in top_n(counts, n):
        print(f"{item} - {count}")


if __name__ == "__main__":
    main()
