from datetime import datetime
from time import timezone
from tinydb import Query, TinyDB
from config import Settings
from uuid import uuid4
import logging

_log = logging.getLogger(__name__)

settings = Settings()


class CRUD:
    def __init__(self, db: TinyDB | None = None, table: str | None = None):
        self.db = db
        self.query = Query()
        self.table = table

    def get_all_my_data(self):
        if not self.db:
            self.init_db
        if self.table:
            self.db = self.table
        return self.db.all()

    def get_ethan_user(self):
        if not self.db:
            self.init_db
        if self.table:
            self.db = self.table
        return self.db.get(Query().id == "ethan")

    def lookup_user(self, username: str):
        """return user if username present in users table"""
        if not self.db:
            self.init_db
        if self.table == "users":
            self.db = self.table
        else:
            _log.error(
                "Attempted to lookup user without providing proper table. Expected 'users' got %s",
                self.table,
            )

        return self.table.get(Query().username == username)

    def insert_user(self, username: str, password: str):
        if not self.db:
            self.init_db
        if self.table:
            self.db = self.table
        user = {
            "id": str(uuid4()),
            "username": username,
            # this password should be sha256 encrypted on the frontend
            "password": password,
        }
        _log.debug("Inserting new user %s", user)
        self.db.insert(user)

    def create_session(self, user_id):
        if not self.db:
            self.init_db
        if self.table:
            self.db = self.table
        session_id = str(uuid4())
        self.db.insert(
            {
                "user_id": user_id,
                "session_id": session_id,
                "created": str(datetime.utcnow()),
                "accessed": str(datetime.utcnow()),
            }
        )
        return session_id

    @property
    def init_db(self):
        path = str(settings.DATA_DIR / "data.json")
        self.db = TinyDB(path, sort_keys=True, indent=4, separators=(",", ": "))
        return self.db

    @classmethod
    def with_table(cls, table_name: str):
        """returns a new instance of CRUD class with a db instance set to provided table_name"""
        crud = cls()
        _db = crud.init_db
        _table = _db.table(table_name)
        return cls(db=_db, table=_table)


def main():
    my_db = CRUD().init_db
    my_db.truncate()
    users = my_db.table("users")
    users.truncate()
    users.insert(
        {
            "id": "ethan",
            "username": "psnethan@gmail.com",
            "balances": [{"name": "emergency", "balance": 1000}],
            "net_monthly_income": 5000,
            "needs": [{"name": "total", "amount": 2000}],
            "debts": [{"name": "total", "balance": 12000, "min_monthly": 300}],
        }
    )


if __name__ == "__main__":
    main()
