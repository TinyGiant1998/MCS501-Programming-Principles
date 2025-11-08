# Formula to convert Celsius to Fahrenheit
def c_to_f(celsius: float) -> float:
    return (celsius * 9 / 5) + 32


# Formula to convert Fahrenheit to Celsius
def f_to_c(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5 / 9


menu_text = """
Temprature Coversion
--------------------
1. Convert into Fahrenheit
2. Convert into Celsius
3. Exit
--------------------

Please Enter your choice 1, 2 or 3
"""


# Making a function to dynamically take a converter and the corresponding unit label
def convert_temprature(converter, from_unit: str, to_unit: str):
    while True:
        try:
            value = float(input(f"Enter temprature {from_unit}: "))
        except ValueError:
            print("🔴 Please enter a valid number. \n")
            continue

        converted = converter(value)
        print(f"{value:.2f}°{from_unit} is {converted:.2f}°{to_unit}\n")

        while True:
            again = (
                input(f"Convert another {from_unit} to {to_unit}? (y/n): ")
                .strip()
                .lower()
            )

            if again == "y":
                break
            elif again == "n":
                return
            else:
                print("Please press 'y' for Yes or 'n' for No.\n")


def main():
    while True:
        choice = input(menu_text).strip()

        if choice not in {"1", "2", "3"}:
            print("🔴Invalid - Please enter 1, 2 or 3. \n")
            continue

        if choice == "3":
            print("👋 Goodbye!")
            break

        if choice == "1":
            convert_temprature(c_to_f, "Celsius", "Fahrenheit")
        elif choice == "2":
            convert_temprature(f_to_c, "Fahrenheit", "Celsius")


if __name__ == "__main__":
    main()
