from datetime import datetime, timedelta


def compute_boundary(days):
    return (datetime.today() - timedelta(days=days)).timestamp()


def timestamp_from_time(time):
    datetime_ = datetime.fromisoformat(time.split("+")[0])
    return datetime_.timestamp()
