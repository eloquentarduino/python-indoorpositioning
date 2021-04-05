import re
from subprocess import check_output
from indoorpositioning.scanner.BaseScanner import BaseScanner


class LinuxWifiScanner(BaseScanner):
    """
    Scan WiFi networks on Linux (requires iwlist)
    """
    def __init__(self, interface, sudo=True):
        """
        Constructor
        :param interface: str WiFi interface
        :param sudo: bool if use sudo or not (you probably want sudo)
        """
        self.interface = interface
        self.sudo = sudo

    def scan(self, sudo=False):
        """
        Scan
        :return:
        """
        iwlist = ['iwlist', self.interface, 'scan']

        if self.sudo:
            iwlist = ['sudo'] + iwlist

        return self.parse(check_output(iwlist).decode('utf-8'))

    def parse(self, iwlist_output):
        """
        Parse iwlist result
        :param iwlist_output: str
        :return:
        """
        access_points = {}

        for cell in iwlist_output.split('Cell'):
            match = re.search(r'Signal level=(-?\d+)[\s\S]+ESSID:"([^"]+)"', cell, re.IGNORECASE)

            if match is None:
                continue

            ssid = match.groups()[1].strip()
            rssi = int(match.groups()[0])

            access_points.setdefault(ssid, rssi)

        return access_points
