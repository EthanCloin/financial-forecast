from tinydb import Query, TinyDB, where
from config import Settings

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
    users.insert(
        {
            "id": "ethan",
            "balances": [{"name": "emergency", "balance": 1000}],
            "net_monthly_income": 5000,
            "needs": [{"name": "total", "amount": 2000}],
            "debts": [{"name": "total", "balance": 12000, "min_monthly": 300}],
        }
    )


if __name__ == "__main__":
    main()
