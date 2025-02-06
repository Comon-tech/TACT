from typing import ClassVar

from pydantic import NonNegativeInt, PositiveInt

from .database import Model


# ----------------------------------------------------------------------------------------------------
# * DbUser
# ----------------------------------------------------------------------------------------------------
class DbUser(Model, collection_name="users"):
    id: int
    xp: NonNegativeInt = 0
    level: PositiveInt = 1
    inventory: list[str] = []

    MAX_LEVEL: ClassVar = 61
    ROLES: ClassVar = [
        ("Intermediate", 3),
        ("Novice", 9),
        ("Techie", 16),
        ("Geek", 23),
        ("Hacker", 30),
        ("Guru", 37),
        ("King", 49),
        ("Wizard", MAX_LEVEL),
    ]

    def draw_level_progress_bar(self, length=5, on_icon="⭐", off_icon="☆") -> str:
        normalized_level = int((self.level / self.MAX_LEVEL) * length)
        return (normalized_level * on_icon) + ((length - normalized_level) * off_icon)

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


# ----------------------------------------------------------------------------------------------------
# * Indexes
# ----------------------------------------------------------------------------------------------------
DbUser.COLLECTION.create_index("id", unique=True)
