"""
This file contains examples of how to use the Tourist class.

:copyright: (c) 2021 - 2023 Dominic H. (https://amigoingonholiday.co.uk)
:license: GNU GPL v3.0, see LICENSE for more details.
"""
from tourist import Tourist

client = Tourist()
global_totals = client.get_global_totals()

if __name__ == "__main__":
    # Get the global totals
    print(f"Total new cases: {client.format_number(global_totals['total_new_cases'])}")
    print(f"Total cases: {client.format_number(global_totals['total_cases'])}")
    print(f"Total new deaths: {client.format_number(global_totals['total_new_deaths'])}")
    print(f"Total deaths: {client.format_number(global_totals['total_deaths'])}")
    print(f"Last updated: {global_totals['timestamp']}")

    # Get border restrictions for Switzerland
    restrictions = client.get_travel_restrictions("France")
    print(f"Restriction level: {restrictions['restriction_level']}")
    print(f"Restriction description: {restrictions['restriction_description']}")

    # Get the total cases for Switzerland between 2020-01-01 and 2023-03-31
    print(f"Total cases for Switzerland between 2020-01-01 and 2020-03-31: "
          f"{client.format_number(client.get_total_cases('CH', '2020-01-01', '2020-03-31'))}")

    # Get the total deaths for Switzerland between 2020-01-01 and 2023-03-31
    print(f"Total deaths for Switzerland between 2020-01-01 and 2020-03-31: "
          f"{client.format_number(client.get_total_deaths('CH', '2020-01-01', '2020-03-31'))}")
