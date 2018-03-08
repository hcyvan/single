from enum import IntEnum


class LoveStatus(IntEnum):
    on = 1
    agree = 2
    reject = 3
    mask = 4


class NoticeType(IntEnum):
    receive_love = 1
    love_handled = 2


class NoticeStatus(IntEnum):
    unread = 1
    read = 2


INIT_POINT = 10
