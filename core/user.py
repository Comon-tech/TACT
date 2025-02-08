from typing import ClassVar

from pydantic import NonNegativeInt, PositiveInt

from .database import Model
from .utils import draw_utf8_progress_bar


# ----------------------------------------------------------------------------------------------------
# * DbUser
# ----------------------------------------------------------------------------------------------------
class DbUser(Model, collection_name="users"):
    id: int  # discord id
    xp: NonNegativeInt = 0
    level: PositiveInt = 1
    gold: NonNegativeInt = 0
    items: list[str] = []

    MAX_LEVEL: ClassVar[int] = 61
    ROLES: ClassVar[list] = [
        ("Intermediate", 3),
        ("Novice", 9),
        ("Techie", 16),
        ("Geek", 23),
        ("Hacker", 30),
        ("Guru", 37),
        ("King", 49),
        ("Wizard", MAX_LEVEL),
    ]

    @property
    def next_level_xp(self):
        return 1000 + (self.level - 1) ** 2 * 1000

    @property
    def role_name(self):
        for role_name, level_threshold in self.ROLES:
            if self.level <= level_threshold:
                return role_name
        return None

    def try_level_up(self):
        if self.xp >= self.next_level_xp:
            self.level += 1
            return True
        return False

    def draw_level(self) -> str:
        return draw_utf8_progress_bar(self.level, self.MAX_LEVEL, 5, "⭐", "☆")

    def draw_xp(self) -> str:
        return draw_utf8_progress_bar(self.xp, self.next_level_xp, 10, "■", "□")


# ----------------------------------------------------------------------------------------------------
# * Indexes
# ----------------------------------------------------------------------------------------------------
DbUser.COLLECTION.create_index("id", unique=True)
