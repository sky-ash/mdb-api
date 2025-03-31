from fastapi import HTTPException

ERROR_DETAILS = {
    204: "No content (no matching data found)",
    401: "Invalid credentials",
    500: "Internal server error",
    504: "Gateway timeout"
}

def raise_http_error(status_code: int):
    detail = ERROR_DETAILS.get(status_code, "Unexpected error")
    raise HTTPException(status_code=status_code, detail=f"Error {status_code}: {detail}")


import requests
from app.env import MDB_DATA_BASE_URL, MDB_DATA_READ_TOKEN, TIMEOUT

def process_request(name: str):
    try:
        response = requests.get(
            url=f"{MDB_DATA_BASE_URL}/api/v1/byName",
            params={"apikey": MDB_DATA_READ_TOKEN, "name": name},
            timeout=TIMEOUT
        )

        # print the config values only if needed for debugging (uncomment the following lines)
        # print(f"MDB_DATA_BASE_URL: {MDB_DATA_BASE_URL}")
        # print(f"MDB_DATA_READ_TOKEN: {MDB_DATA_READ_TOKEN}")
        # print(f"TIMEOUT: {TIMEOUT}")

        # if mdb-data returns a status code other than 200 (can only be 401, or something unexpected)
        if response.status_code != 200:
            raise_http_error(response.status_code)

        # otherwise, if the status code is 200, load the response data
        data = response.json()

        # check integrity of the response data (raise internal server error if data is faulty)
        if data is None or "records" not in data or "data" not in data:
            raise_http_error(500)

        # check if the query returned any results
        if data["records"] == 0:
            raise_http_error(204)

        # filter each entry in the body of the response for the required fields
        data["data"] = [
            {"id": person["id"], "titel": person["titel"]}
            for person in data["data"]
        ]

        return data # returns the entire response, including headers, but with filtered body

    except requests.Timeout:
        raise_http_error(504)
    except requests.RequestException:
        raise_http_error(500)

