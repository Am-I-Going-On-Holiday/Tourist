# API response snapshot (archive)

This directory contains a snapshot of the API responses from the [covid19api.com](https://covid19api.com) service. The responses are grouped by the endpoint.

| Endpoint Group   | Description            |
| ---------------- | ---------------------- |
| `internal`       | Internal API endpoints |
| `premium`        | Endpoints requiring a premium subscription to access |
| `standard`       | Endpoints available to all users |


## Snapshot information
The API does have a large database of countries (see [`standard/countries.json`](standard/countries.json)), but the snapshot was taken with Switzerland as the default country. This was done to reduce the size of the overall snapshot.

The dates given for `*_date_range` start at `2020-03-01` and end at `2020-04-01`. Once again, this was done to reduce the size of the overall snapshot.