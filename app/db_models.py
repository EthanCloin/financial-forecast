from datetime import datetime, timezone, timedelta
from uuid import uuid4
from pydantic import BaseModel


class User(BaseModel):
    id: str = str(uuid4())
    username: str
    password: str
    balances: list[dict] = []
    net_monthly_income: int = 0
    needs: list[dict] = []
    debts: list[dict] = []


# tinydb does not play nice with pydantic bc it wants everything to
# be json serialized, disallowing uuid and datetime types
class Session(BaseModel):
    session_id: str = str(uuid4())
    user_id: str = str(uuid4())
    created: str = datetime.now(timezone.utc).isoformat()
    modified: str = datetime.now(timezone.utc).isoformat()
    expires: str = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()

    def is_session_expired(self) -> bool:
        now = datetime.now(timezone.utc)
        expires = datetime.fromisoformat(self.expires)
        return expires < now

    def refresh_session(self):
        modified = datetime.now(timezone.utc)
        expires = modified + timedelta(days=2)

        self.modified = modified.isoformat()
        self.expires = expires.isoformat()
        return self
