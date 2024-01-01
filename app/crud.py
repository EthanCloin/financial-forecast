from datetime import datetime
import security
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
        return user

    def create_session(self, user_id):
        if not self.db:
            self.init_db
        if self.table:
            self.db = self.table
        session_id = str(uuid4())
        new_session = {
            "user_id": user_id,
            "session_id": session_id,
        }

        new_session = security.add_new_session_times(new_session)
        self.db.insert(new_session)
        return new_session

    def get_user_from_session(self, session_id):
        if not self.db:
            self.init_db

        users = self.db.table("users")
        sessions = self.db.table("sessions")

        cur_session = sessions.get(Query().session_id == session_id)
        cur_user = users.get(Query().id == cur_session["user_id"])
        return cur_user

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
            "password": "$pbkdf2-sha256$29000$PgcgxPjf27sXwhjDWOv9Xw$ly31FFuPlaq4V9g7cc8jJkZt2OMbM21nJLgzQkHxFPM",
            "balances": [{"name": "emergency", "balance": 1000}],
            "net_monthly_income": 5000,
            "needs": [{"name": "total", "amount": 2000}],
            "debts": [{"name": "total", "balance": 12000, "min_monthly": 300}],
        }
    )
    # sessions = my_db.table("sessions")
    # sessions.insert({})


if __name__ == "__main__":
    main()
