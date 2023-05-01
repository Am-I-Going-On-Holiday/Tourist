"""
Tourist: API Client for the covidapi.com API service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic Usage (Cases):
>>> from tourist import Tourist
>>> covid = Tourist()
>>> covid.get_total_cases('CH', '2020-03-01', '2020-03-31')
17909

... or for getting border restrictions:
>>> restrictions_fr = covid.get_travel_restrictions('FR')
>>> restrictions_fr['restriction_description']
Level 3: Ban arrivals from some regions

:copyright: (c) 2021 - 2023 Dominic H. (https://amigoingonholiday.co.uk)
:license: GNU GPL v3.0, see LICENSE for more details.
"""
import requests
import json
import datetime
import iso8601
from requests import RequestException
from urllib3.exceptions import InsecureRequestWarning

""" Disable SSL Warnings """
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class Tourist:
    def __init__(self) -> None:
        """
        Set access token and headers
        """
        self.access_token = "REPLACE-ME"  # replace with your own access token
        self.headers = {
            'X-Access-Token': self.access_token,
            'User-Agent': 'TouristBot/1.1',
            'Accept': 'application/json'
        }

    def make_request(self, endpoint: str) -> dict:
        """
        Make a request to the API

        :param str endpoint: The endpoint to make the request to
        :return: The response from the API
        """
        try:
            endpoint_request = requests.get(f"https://api.covid19api.com/{endpoint}", headers=self.headers,
                                            verify=False)
            endpoint_response = json.loads(endpoint_request.text)
            return endpoint_response
        except RequestException as e:
            return e

    def to_date_fix(self, to_date: str) -> datetime:
        """
        Fix the to_date if it is today - workaround for API data collection issues

        :param to_date: End date of date range in ISO format (i.e. 2020-01-31)
        :return: Returns subtracted date if to_date is today and before 12:00, else returns to_date
        """
        if to_date == datetime.datetime.now().strftime("%Y-%m-%d") and datetime.datetime.now().hour < 12:
            return datetime.datetime.now() - datetime.timedelta(days=1)

        return to_date

    def get_cases(self, country: str, from_date: str, to_date: str) -> list:
        """
        Get the cases for a country within a date range

        :param str country: Country to get the cases for (i.e. France, FR)
        :param str from_date: Start date of date range in ISO format (i.e. 2020-01-01)
        :param str to_date: End date of date range in ISO format (i.e. 2020-01-31)
        :return: Case dates and counts for each day in the date range
        """
        cases = []

        for case in self.make_request(f"premium/country/{country}?from={from_date}&to={self.to_date_fix(to_date)}"):
            cases.append({
                'date': iso8601.parse_date(case['Date']).strftime("%d/%m/%Y"),
                'confirmed': case['NewCases'],
            })

        return cases

    def get_total_cases(self, country: str, from_date: str, to_date: str) -> int:
        """
        Get the total cases for a country within a date range

        :param str country: Country to get the total cases for (i.e. France, FR)
        :param str from_date: Start date of date range in ISO format (i.e. 2020-01-01)
        :param str to_date: End date of date range in ISO format (i.e. 2020-01-31)
        :return: The total cases for the country within the date range
        """
        total_cases = 0

        for case in self.make_request(f"premium/country/{country}?from={from_date}&to={to_date}"):
            total_cases += case['NewCases']

        return total_cases

    def get_deaths(self, country: str, from_date: str, to_date: str) -> list:
        """
        Get the deaths for a country within a date range

        :param str country: Country to get the deaths for (i.e. France, FR)
        :param str from_date: Start date of date range in ISO format (i.e. 2020-01-01)
        :param str to_date: End date of date range in ISO format (i.e. 2020-01-31)
        :return: Death dates and counts for each day in the date range
        """
        deaths = []

        for death in self.make_request(f"premium/country/{country}?from={from_date}&to={self.to_date_fix(to_date)}"):
            deaths.append({
                'date': iso8601.parse_date(death['Date']).strftime("%d/%m/%Y"),
                'confirmed': death['NewDeaths'],
            })

        return deaths

    def get_total_deaths(self, country: str, from_date: str, to_date: str) -> int:
        """
        Get the total deaths for a country within a date range

        :param str country: Country to get the total deaths for (i.e. France, FR)
        :param str from_date: Start date of date range in ISO format (i.e. 2020-01-01)
        :param str to_date: End date of date range in ISO format (i.e. 2020-01-31)
        :return: The total deaths for the country within the date range
        """
        total_deaths = 0

        for death in self.make_request(f"premium/country/{country}?from={from_date}&to={to_date}"):
            total_deaths += death['NewDeaths']

        return total_deaths

    def get_travel_restrictions(self, country: str) -> dict:
        """
        Get the travel border_restrictions for a country

        :param country: Country to get the travel border_restrictions for (i.e. France, FR)
        :return: The travel border_restrictions
        """
        restrictions_data = self.make_request(f"premium/travel/country/{country}")

        border_restrictions = {
            'restriction_level': restrictions_data['Level']['Level'],
            'restriction_description': restrictions_data['Level']['LevelDesc'],
            'timestamp': iso8601.parse_date(restrictions_data['Country']['Timestamp']).strftime(
                "%d/%m/%Y at %H:%M GMT"),
        }

        return border_restrictions

    def get_global_totals(self) -> dict:
        """
        Get the global pandemic case and death totals

        :return: The global totals (confirmed new cases, deaths in the last 24h as well as all-time totals)
        """
        summary_data = self.make_request("summary")['Global']

        summary = {
            'total_new_cases': summary_data['NewConfirmed'],
            'total_cases': summary_data['TotalConfirmed'],
            'total_new_deaths': summary_data['NewDeaths'],
            'total_deaths': summary_data['TotalDeaths'],
            'timestamp': iso8601.parse_date(summary_data['Date']).strftime("%d/%m/%Y at %H:%M GMT"),
        }

        return summary

    def format_number(self, number: int) -> str:
        """
        Format a number with commas

        :param int number: Number to format
        :return: Formatted number
        """
        return f"{number:,}"

    def round_to_nearest(self, number: int, nearest: int) -> int:
        """
        Round a number to the nearest given number

        :param int number: Number to round
        :param int nearest: Number to round to
        :return: Rounded number
        """
        return int(nearest * round(float(number) / nearest))
