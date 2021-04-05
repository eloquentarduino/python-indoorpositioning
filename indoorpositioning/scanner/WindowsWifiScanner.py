import re
from subprocess import check_output
from indoorpositioning.scanner.BaseScanner import BaseScanner


class WindowsWifiScanner(BaseScanner):
    """
    Scan WiFi networks on Windows (requires netsh)
    """
    def scan(self):
        """
        Scan
        :return: dict
        """
        return self.parse(check_output(['netsh', 'wlan', 'show', 'networks', 'mode=bssid']).decode('utf-8'))

    def parse(self, netsh_output):
        """
        Parse netsh result
        :param netsh_output: str
        :return:
        """
        access_points = {}

        for cell in re.split(r'[^B]SSID\s+\d+\s*:', ' ' + netsh_output):
            match = re.search(r'^([^\n]+)\n[\s\S]+:\s+(\d+)%', cell.strip(), re.IGNORECASE)

            if match is None:
                continue

            ssid = match.groups()[0].strip()
            rssi = int(match.groups()[1])

            access_points.setdefault(ssid, rssi)

        return access_points
