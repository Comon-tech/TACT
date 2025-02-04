import asyncio
import random
from typing import ClassVar, Sequence

import discord
from discord import Guild, Member, Message, Role, User, utils
from pydantic import PositiveInt

from .model import Model


# ----------------------------------------------------------------------------------------------------
# * DbUser
# ----------------------------------------------------------------------------------------------------
class DbUser(Model):
    _collection = Model._database["users"]
    id: int
    xp: PositiveInt = 0
    level: PositiveInt = 1
    inventory: list[str] = []

    @property
    def next_level_xp(self):
        return 1000 + (self.level - 1) ** 2 * 1000

    @property
    def role_name(self):
        level_to_role = {
            range(1, 3): "Intermediate",
            range(4, 9): "Novice",
            range(11, 16): "Techie",
            range(17, 23): "Geek",
            range(24, 30): "Hacker",
            range(31, 37): "Guru",
            range(43, 49): "King",
            range(55, 61): "Wizard",
        }
        for level_range, role_name in level_to_role.items():
            if self.level in level_range:
                return role_name
        return None

    def try_level_up(self):
        if self.xp >= self.next_level_xp:
            self.level += 1
            return True
        return False

    async def award_role(self, user: User | Member):
        if self.role_name:
            role = utils.get(user.guild.roles, name=self.role_name)
            if role and role not in user.roles:
                await user.add_roles(role)
                return role
        return None
