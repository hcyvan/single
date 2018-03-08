from enum import IntEnum


class LoveStatus(IntEnum):
    on = 1
    agree = 2
    reject = 3
    mask = 4
    part = 5


class NoticeType(IntEnum):
    love_on = 1
    love_agree = 2
    love_reject = 3
    love_mask = 4
    love_part = 5


class NoticeStatus(IntEnum):
    unread = 1
    read = 2


INIT_POINT = 10
