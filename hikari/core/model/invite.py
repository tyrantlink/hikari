#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © Nekoka.tt 2019
#
# This file is part of Hikari.
#
# Hikari is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hikari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Hikari. If not, see <https://www.gnu.org/licenses/>.
"""
Invitations to guilds.
"""
from __future__ import annotations

import dataclasses
import datetime
import typing

from hikari.core.model import channel
from hikari.core.model import guild
from hikari.core.model import model_cache
from hikari.core.model import user
from hikari.core.utils import dateutils


@dataclasses.dataclass()
class Invite:
    """
    Represents a code that when used, adds a user to a guild or group DM channel.
    """

    __slots__ = ("_state", "code", "guild", "channel", "approximate_presence_count", "approximate_member_count")

    _state: typing.Any

    #: The unique invite code
    #:
    #: :type: :class:`str`
    code: str

    #: The guild the invite is for
    #:
    #: :type: :class:`hikari.core.model.guild.Guild`
    guild: guild.Guild

    #: The channel the invite points to
    #:
    #: :type: :class:`hikari.core.model.channel.GuildChannel`
    channel: channel.GuildChannel

    #: Approximate count of online members.
    #:
    #: :type: :class:`int` or `None`
    approximate_presence_count: typing.Optional[int]

    #: Approximate count of total members.
    #:
    #: :type: :class:`int` or `None`
    approximate_member_count: typing.Optional[int]

    def __init__(self, global_state: model_cache.AbstractModelCache, payload):
        self._state = global_state
        self.code = payload.get("code")
        self.guild = global_state.parse_guild(payload.get("guild"))
        self.channel = global_state.parse_channel(payload.get("channel"))
        self.approximate_presence_count = transform.get_cast(payload, "approximate_presence_count", int)
        self.approximate_member_count = transform.get_cast(payload, "approximate_member_count", int)


@dataclasses.dataclass()
class InviteMetadata:
    """
    Metadata relating to a specific invite object.
    """

    __slots__ = ("_state", "inviter", "uses", "max_uses", "max_age", "temporary", "created_at", "revoked")

    _state: typing.Any

    #: The user who created the invite.
    #:
    #: :type: :class:`hikari.core.model.user.User`
    inviter: user.User

    #: The number of times the invite has been used.
    #:
    #: :type: :class:`int`
    uses: int

    #: The maximum number of times the invite may be used.
    #:
    #: :type: :class:`int`
    max_uses: int

    #: Duration after which the invite expires, in seconds.
    #:
    #: :type: :class:`int`
    max_age: int

    #: Whether or not the invite only grants temporary membership.
    #:
    #: :type: :class:`bool`
    temporary: bool

    #: When the invite was created.
    #:
    #: :type: :class:`datetime.datetime`
    created_at: datetime.datetime

    #: Whether or not the invite has been revoked.
    #:
    #: :type: :class:`bool`
    revoked: bool

    def __init__(self, global_state: model_cache.AbstractModelCache, payload):
        self._state = global_state
        self.inviter = global_state.parse_user(payload.get("inviter"))
        self.uses = transform.get_cast(payload, "uses", int)
        self.max_uses = transform.get_cast(payload, "max_uses", int)
        self.max_age = transform.get_cast(payload, "max_age", int)
        self.temporary = transform.get_cast(payload, "temporary", bool)
        self.created_at = transform.get_cast(payload, "created_at", dateutils.parse_iso_8601_datetime)
        self.revoked = transform.get_cast(payload, "revoked", bool)


__all__ = ["Invite", "InviteMetadata"]
