from datetime import datetime


def str_to_date(val: str) -> datetime.date:
    return datetime.strptime(val, '%Y-%m-%d').date()


def is_start_before_end(start: datetime.date, end: datetime.date):
    return start and end and start < end
