from requests import models, get
from hashlib import sha1
from getpass import getpass
from sys import exit


def request_api_data(query_char: str) -> models.Response:
    url: str = "https://api.pwnedpasswords.com/range/"
    res: models.Response = get(f"{url}{query_char}")
    if res.status_code != 200:
        raise RuntimeError("Error fetching data")
    return res


def get_hashed_pass() -> str:
    return sha1(str(getpass()).encode("utf-8")).hexdigest().upper()


def check_password(api_data: models.Response, hashpassend: str) -> str:
    hashedentry: str
    num_times: str
    for entry in api_data.text.splitlines():
        hashedentry, num_times = entry.split(":")
        if hashedentry == hashpassend:
            return f"Password has been seen {int(num_times):,} times before."
    return "Password has not been found."


def main() -> None:
    hashed_pass = get_hashed_pass()
    head: str = hashed_pass[:5]
    tail: str = hashed_pass[5:]
    print(check_password(request_api_data(head), tail))


if __name__ == '__main__':
    exit(main())
