from gradebook_lite.core import validates_scores, mean, min_max, letter_grade


def parse_input(raw: str):
    try:
        return [float(s.strip()) for s in raw.split(",")]
    except ValueError:
        raise ValueError("All input must be number")


def main():
    print("=== Gradebook Lite===")

    while True:
        raw = input("Enter scores (comma sperated): ").strip()

        try:
            scores = parse_input(raw)
            scores = validates_scores(scores)
        except ValueError as e:
            print(f"Error {e}")
            print("Please try again\n")
            continue

        count = len(scores)
        min_score, max_score = min_max(scores)
        average = mean(scores)
        grade = letter_grade(average)

        print(f"\nCount: {count}")
        print(f"Min/Max: {min_score} / {max_score}")
        print(f"Mean: {average:.2f}")
        print(f"Final grade: {grade}\n")

        again = input("Another set? (y/n): ").lower().strip()
        if again != "y":
            print("Goodbye ...")
            break


if __name__ == "__main__":
    main()
