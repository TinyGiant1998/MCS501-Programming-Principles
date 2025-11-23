import datetime
import random

# Zone Fares
zones = {
    "Zone1": 2.80,
    "Zone2": 4.50,
    "Zone3": 6.20,
}

# Stations mapped to Zone
stations = {
    "Central": "Zone1",
    "Harbour": "Zone1",
    "Airport": "Zone2",
    "Hills": "Zone3",
}

card = {
    "balance": 20.00,
    "autotopup_enabled": "On",
    "autotopup_amount": 20,
    "in_trip": False,
    "tap_on_station": None,
    "tap_on_time": None,
}

available_stations = ", ".join(sorted(stations.keys()))
station_prompt = f"Enter station ({available_stations}): "
trip_log = []
off_peak_discount = 0.25
random_inspection_chance = 10

# Converting into minutes to make comparision easier
# Peak hours: 07:00–09:30 and 16:00–18:30
peak_morning_start = 7 * 60
peak_morning_end = 9 * 60 + 30
peak_evening_start = 16 * 60
peak_evening_end = 18 * 60 + 30

menu_item = """
-------------------------------------------------
Please choose a command:
1. View card status
2. Toggle auto top-up on/off
3. Set auto top-up amount
4. Tap ON at a station
5. Tap OFF at a station
6. View trip and charge summary (this session)
7. Exit
-------------------------------------------------
"""

# Main loop
while True:
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M")
    current_minute = now.hour * 60 + now.minute

    in_peak = (peak_morning_start <= current_minute <= peak_morning_end) or (
        peak_evening_start <= current_minute <= peak_evening_end
    )
    period = "Peak" if in_peak else "Off-Peak"

    print(f"**** Context **** \nTime now: {time_str} \nPeriod: {period} \n {menu_item}")

    choice = input("Please enter a menu option between 1 to 7: \n")

    if choice == "":
        print("Please enter a menu option between 1 to 7: \n")
        continue

    if not choice.isdigit() or choice not in {"1", "2", "3", "4", "5", "6", "7"}:
        print("Invalid choice. Please enter a digit between 1 and 7. \n")
        continue

    if choice == "1":
        print(
            f"\nYour Balance: ${card['balance']:.2f} \nAuto Top-up Status: {card['autotopup_enabled']} \nAuto Top-up Amount: ${card['autotopup_amount']:.2f} \nIn-Trip: {card['in_trip']}\n"
        )
        continue

    if choice == "2":
        card["autotopup_enabled"] = "Off" if card["autotopup_enabled"] == "On" else "On"
        print(f"Auto Top-up now: {card['autotopup_enabled']}\n")
        continue

    if choice == "3":
        while True:
            amount = input("Enter Auto Top-up amount: ").strip()
            if not amount or not amount.isdigit() or int(amount) <= 0:
                print("Please enter a valid amount to top-up. For eg. 10 or 20:")
                continue

            card["autotopup_amount"] = int(amount)
            print(f"Auto top-up amount set to ${card['autotopup_amount']}\n")
            break
        continue

    if choice == "4":
        if card["in_trip"]:
            print(
                f"You have already tapped On at {card['tap_on_station']} (Tap On time: {card['tap_on_time']})"
            )
            continue

        while True:
            user_station = input(station_prompt).lower().strip()

            if user_station == "":
                print(f"Please enter a station name ({available_stations}): ")
                continue

            tap_on_dest = None
            for st in stations:
                if st.lower() == user_station:
                    tap_on_dest = st
                    break

            if not tap_on_dest:
                print(
                    f"Station not found. Please enter a valid station name - ({available_stations})"
                )
                continue

            card["in_trip"] = True
            card["tap_on_station"] = tap_on_dest
            card["tap_on_time"] = now.strftime("%H:%M")
            print(
                f"Tapped On at {tap_on_dest} - {stations[tap_on_dest]} at {card["tap_on_time"]}.\n"
            )
            break
        continue

    if choice == "5":
        while True:
            if not card["in_trip"]:
                print("You are not currently in a trip. (Tap ON first)")
                inspect_roll = random.randint(0, 99)
                warning_or_not = (
                    "Inspection: Irregular activity detected. Penalty warning issued.\n"
                    if inspect_roll < random_inspection_chance
                    else "Inspection: Irregular activity noted. Please tap ON next time.\n"
                )
                print(warning_or_not)
                break

            user_station = input(station_prompt).lower().strip()
            if user_station == "":
                print(f"Please enter a station name ({available_stations}): ")
                continue

            tap_off_dest = None
            for st in stations:
                if st.lower() == user_station:
                    tap_off_dest = st
                    break

            if not tap_off_dest:
                print(
                    f"Station not found. Please enter a valid station name - ({available_stations})"
                )
                continue

            card["tap_off_dest"] = tap_off_dest

            # Fare calculation
            origin = card["tap_on_station"]
            destination = card["tap_off_dest"]
            origin_zone = stations[origin]  # type: ignore
            destination_zone = stations[destination]

            base_fare = max(zones[origin_zone], zones[destination_zone])
            fare = base_fare

            if period == "Off-Peak":
                fare = round(base_fare * (1 - off_peak_discount), 2)
            else:
                fare = round(base_fare, 2)

            charged = fare

            # Handle balance and top-up
            if card["balance"] < charged:
                if card["autotopup_enabled"] == "On":
                    topup_amount = card["autotopup_amount"]
                    card["balance"] += float(topup_amount)
                    print(
                        f"Automation triggered: Auto Top-up +${topup_amount:.2f} applied."
                    )
                    card["balance"] -= charged
                else:
                    card["balance"] -= charged
                    print("Warning: Your card balance is negative. Please top-up")
            else:
                card["balance"] -= charged

            # Trip Record
            trip_record = {
                "origin": origin,
                "origin_zone": origin_zone,
                "destination": destination,
                "destination_zone": destination_zone,
                "time": now.strftime("%H:%M"),
                "period": period,
                "fare": charged,
            }
            trip_log.append(trip_record)

            # Output
            print(
                f"Trip: {origin} ({origin_zone}) -> {destination} ({destination_zone}) | Period: {period}"
            )
            print(f"Fare charged: ${charged:.2f}")
            print(f"Current balance: ${card['balance']:.2f}")

            inspect_roll = random.randint(0, 99)
            if inspect_roll < random_inspection_chance:
                print("Inspection: All good. Have a nice day!\n")

            # Reset trip
            card["in_trip"] = False
            card["tap_on_station"] = None
            card["tap_on_time"] = None

            break  # ✅ THIS break exits the while True loop correctly

    if choice == "6":
        if not trip_log:
            print("\nNo Trips this session \n")
            continue

        print("\nTrips this session:")
        total_spent = 0.0
        for idx, t in enumerate(trip_log, start=1):
            print(
                f"{idx} {t['origin']} -> {t['destination']} | {t['period']} | ${t['fare']:.2f}"
            )
            total_spent += float(t["fare"])

        print(f"Total spent: ${total_spent:.2f}\n")
        continue

    if choice == "7":
        print("Exiting MetroTicketSim. See you next time 👋")
        break
