import re
from subprocess import check_output
from indoorpositioning.scanner.BaseScanner import BaseScanner


class OSXWifiScanner(BaseScanner):
    """
    Scan WiFi networks on OS X
    """
    def scan(self):
        """
        Scan
        :return:
        """
        airport = check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport', '-s'])

        return self.parse(airport.decode('utf-8'))

    def parse(self, airport_output):
        """
        Parse airport -s output
        :param airport_output: str
        :return:
        """
        access_points = {}

        for line in airport_output.split('\n'):
            # strcuture is SSID MAC RSSI
            match = re.search(r'^(.+?)\s+([0-9A-F]{2}[:-]){5}([0-9A-F]{2})\s+(-?\d+)\s', line, re.IGNORECASE)

            if match is None:
                continue

            ssid = match.groups()[0].strip()
            rssi = int(match.groups()[-1])

            access_points.setdefault(ssid, rssi)

        return access_points
