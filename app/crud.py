from db_models import User, Session
from tinydb import Query, TinyDB
from tinydb.table import Table
from config import Settings
import logging

_log = logging.getLogger(__name__)
_log.setLevel("DEBUG")
settings = Settings()


class CRUD:
    def __init__(self, db: TinyDB | None = None, table: str | None = None):
        self.db = db
        self.query = Query()
        self.table = table

    def lookup_user(self, username: str) -> User | None:
        """return user if username present in users table"""
        if not self.db:
            self.init_db

        users = self.db.table("users")
        user_db = users.get(Query().username == username)
        if user_db:
            return User.model_validate(user_db)
        return None

    def insert_user(self, username: str, password: str) -> User:
        if not self.db:
            self.init_db

        user = User(username=username, password=password)
        _log.debug("Inserting new user %s", user.model_dump())

        users = self.db.table("users")
        users.insert(user.model_dump())
        return user

    def update_user_balances(self, user_id, balances):
        if not self.db:
            self.init_db

        users: Table = self.db.table("users")
        res = users.update({"balances": balances}, Query().id == user_id)
        print("")

    def create_session(self, user_id) -> Session:
        if not self.db:
            self.init_db

        session = Session(user_id=user_id)
        sessions = self.db.table("sessions")

        _log.debug("Inserting new session %s", session.model_dump())
        sessions.insert(session.model_dump())
        return session

    def delete_session(self, session_id) -> None:
        if not self.db:
            self.init_db
        session = self.db.table("sessions")
        removed = session.remove(Query().session_id == session_id)
        _log.debug("Removed %d session(s)", len(removed))

    def get_user_from_session(self, session_id) -> User | None:
        if not self.db:
            self.init_db

        users = self.db.table("users")
        sessions = self.db.table("sessions")

        db_session = sessions.get(Query().session_id == session_id)
        if db_session:
            cur_session = Session.model_validate(db_session)
            db_user = users.get(Query().id == cur_session.user_id)
            if db_user:
                cur_user = User.model_validate(db_user)
                return cur_user
        return None

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
            "id": "c05f1901-acc9-464a-ae69-4333975c23a4",
            "username": "psnethan@gmail.com",
            "password": "$pbkdf2-sha256$29000$PgcgxPjf27sXwhjDWOv9Xw$ly31FFuPlaq4V9g7cc8jJkZt2OMbM21nJLgzQkHxFPM",
            "balances": [{"name": "emergency", "balance": 1000}],
            "net_monthly_income": 5000,
            "needs": [{"name": "total", "amount": 2000}],
            "debts": [{"name": "total", "balance": 12000, "min_monthly": 300}],
        }
    )
    sessions = my_db.table("sessions")
    sessions.truncate()
    # sessions.insert({})


if __name__ == "__main__":
    main()
