# Tourist
Python API client for the (now defunct) [covid19api.com](https://covid19api.com) service.

## Archival
This project is no longer maintained. The API it was built for is no longer available. The main intention of Tourist was to refactor the existing covid19api.com API client hosted on ['Am I Going On Holiday?'](https://amigoingonholiday.co.uk) to make it more maintainable and easier to extend.

However, the API service announced its deprecation in late April 2023. As such, this project is no longer maintained and is archived.

A copy of all the JSON responses from the API is available in the [`archive`](archive/json/endpoints/) directory.

## Usage
To use Tourist, you will require a valid premium subscription to the covid19api.com service.

After, you can include your API key in the client by modifying the `access_token` variable in `src/client.py`.


## Examples

### Get country cases and deaths

Retrieve the latest COVID-19 statistics for a given country within a given date range.

```python
from tourist import Tourist

client = Tourist()

# Cases
print(client.get_total_cases('Switzerland', '2020-01-01', '2020-03-31'))
>>> 17909

# Deaths
print(client.get_total_deaths('Switzerland', '2020-01-01', '2020-03-31'))
>>> 438
```

### Get border restrictions

Retrieve the latest border restrictions for a given country.

```python
from tourist import Tourist

client = Tourist()

restrictions = client.get_travel_restrictions('France')

# Restriction level code (0-4)
print(restrictions['restrictions_level'])
>>> 3

# Restriction level description
print(restrictions['restrictions_description'])
>>> "Level 3: Ban arrivals from some regions"
```

### Get global totals

Retrieve the latest global case and death totals.

```python
from tourist import Tourist

client = Tourist()

global_totals = client.get_global_totals()

# Global cases (new and total since the start of pandemic)
print(global_totals['total_new_cases'])
>>> 177325
print(global_totals['total_cases'])
>>> 674300711

# Global deaths (new and total since the start of pandemic)
print(global_totals['total_new_deaths'])
>>> 1319
print(global_totals['total_deaths'])
>>> 6793224

# Timestamp of last update (in DD/MM/YYYY HH:MM format)
print(global_totals['timestamp'])
>>> "01/05/2023 at 16:05 GMT"
```

## Data Sources
The data used in this project is sourced from the [covid19api.com](https://covid19api.com) service, where data has been provided by [Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19), [Our World In Data](https://ourworldindata.org/coronavirus) and the [Oxford COVID-19 Government Response Tracker](https://www.bsg.ox.ac.uk/research/research-projects/coronavirus-government-response-tracker).

## License
The code in this project is licensed under the GNU GPLv3 license. See [LICENSE](LICENSE) for more information.

(c) 2021-2023 [Am I Going On Holiday?](https://amigoingonholiday.co.uk) with data from [covid19api.com](https://covid19api.com).