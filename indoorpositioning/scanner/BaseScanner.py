class BaseScanner:
    """
    Abstract base class for a scanner
    """
    def scan(self):
        """
        Scan for nearby access points
        :return: dict {ssid: rssi} pairs
        """
        raise NotImplemented()
