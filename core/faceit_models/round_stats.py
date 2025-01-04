from sqlalchemy.orm import Mapped


class RoundStats:
    Score: Mapped[str]
    Map: Mapped[str]
    Rounds: Mapped[int]
    Region: Mapped[str]
    Winner: Mapped[str]
