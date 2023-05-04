import datetime

def get_current_date_time():
    """Return current datetime

    Returns:
        string: yyyy-mm-dd hh:mm:ss.xxxxxx
    """
    return datetime.datetime.now()


def get_current_time():
    """Return current datetime

    Returns:
        string: hh:mm:ss.xxxxxx
    """
    return datetime.datetime.time(datetime.datetime.now())
