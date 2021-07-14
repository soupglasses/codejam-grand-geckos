import itertools
from dataclasses import dataclass
from typing import Iterator, Optional


@dataclass(eq=True, frozen=True)
class Platform:
    id: int
    name: str


@dataclass
class Credential:
    username: str
    password: str
    id: int
    platform: Platform
    notes: str = ""


class ExampleDB:
    """
    Simple Example database to work with the publiccly facing functions. Not to
    be used in real code.
    """

    _cred_ids = itertools.count()
    _plat_ids = itertools.count()

    def __init__(self):
        self._platforms = {
            "google.com": Platform(next(self._plat_ids), "google.com"),
            "pypi.org": Platform(next(self._plat_ids), "pypi.org"),
        }
        self._db = [
            Credential("sofi", "password", id=next(self._cred_ids), platform=self._platforms["google.com"]),
            Credential("greg", "12345678", id=next(self._cred_ids), platform=self._platforms["google.com"]),
            Credential("bob", "123asd123asd", id=next(self._cred_ids), platform=self._platforms["google.com"]),
            Credential("sofi", "password321", id=next(self._cred_ids), platform=self._platforms["pypi.org"]),
        ]

    @property
    def platforms(self) -> Iterator[Platform]:
        return iter(self._platforms.values())

    @property
    def accounts(self) -> Iterator[Credential]:
        return iter(self._db)

    def match_username(self, username: str) -> Iterator[Credential]:
        return iter(cred for cred in self._db if cred.username == username)

    def match_platform(self, platform: Platform) -> Iterator[Credential]:
        return iter(cred for cred in self._db if cred.platform == platform)

    def match_password(self, password: str) -> Iterator[Credential]:
        return iter(cred for cred in self._db if cred.password == password)

    def search(self, search: str) -> Iterator[Credential]:
        return iter(
            cred
            for cred in self._db
            if search in cred.username or search in cred.platform.name or search in cred.notes
        )

    def add_account(self, username: str, *, password: Optional[str] = None, platform: str):
        if platform not in self._platforms:
            self._platforms[platform] = Platform(next(self._plat_ids), platform)

        plat = self._platforms[platform]
        cred = Credential(username, password or "ENCRYPTED_EXAMPLE", id=next(self._cred_ids), platform=plat)

        self._db.append(cred)

    def remove_account(self, account: Credential):
        if account not in self._db:
            raise Exception("Account does not exist in database.")

        self._db.remove(account)

        # Check if it was the last account for the platform. If so, delete it.
        if not next(self.match_platform(account.platform), None):
            self._platforms.pop(account.platform.name)


if __name__ == "__main__":
    # TODO: Make a better testing system.

    db = ExampleDB()

    from pprint import pprint

    print("Platforms:")
    pprint(list(db.platforms))
    print("Accounts:")
    pprint(list(db.accounts))
    platform = next(db.platforms)
    print('Match username "sofi":')
    pprint(list(db.match_username("sofi")))
    print("Match Platform", platform)
    pprint(list(db.match_platform(platform)))
    print('Match Password "12345678":')
    pprint(list(db.match_password("12345678")))
    print('Search: "google.com":')
    pprint(list(db.search("google.com")))
    db.add_account("sofi@example.com", password="12345678", platform="reddit.com")
    print('Search: "sof":')
    pprint(list(db.search("sof")))
    db.remove_account(next(db.search("sofi@")))
    print('Delete first "sofi@"')
    pprint(list(db.search("sofi@")))
    pprint(list(db.platforms))
