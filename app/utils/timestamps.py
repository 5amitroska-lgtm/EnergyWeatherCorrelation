from datetime import datetime

class Timestamp:
    """
    Represents a simple date (year, month, day) and provides
    conversion utilities.

    Attributes:
        year (int): The year component of the date.
        month (int): The month component of the date.
        day (int): The day component of the date.
    """

    def __init__(self, year, month, day):
        """
        Initialize a Timestamp object.

        Args:
            year (int): The year value.
            month (int): The month value (1–12).
            day (int): The day value (1–31).
        """
        self.year = year
        self.month = month
        self.day = day

    def convert_to_datetime(self):
        """
        Convert the stored date into an ISO‑like datetime string
        with hour set to 00.

        Returns:
            str: A formatted datetime string in the form
                 'YYYY-MM-DDTHH:00:00'.
        """
        date_str = f"{self.year}-{self.month}-{self.day}"
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return str(dt.strftime("%Y-%m-%dT%H:00:00"))


timestamp = Timestamp(2026, 1, 1)
print(timestamp.convert_to_datetime())
