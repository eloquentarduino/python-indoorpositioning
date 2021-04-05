from unittest import TestCase
from indoorpositioning.scanner import *


class TestScanners(TestCase):
    def test_osx_wifi_scanner(self):
        scanner = OSXWifiScanner()
        mock = '''
                     SSID BSSID             RSSI CHANNEL HT CC SECURITY (auth/unicast/group)
              AP1 00:00:00:00:00:00 -100  100     Y  IT WPA2(PSK/AES/AES) 
              AP2 00:00:00:00:00:00 -50  1       Y  IT WPA(PSK/TKIP,AES/TKIP) WPA2(PSK/TKIP,AES/TKIP) 
        '''

        self._assert(scanner.parse(mock))

    def test_linux_wifi_scanner(self):
        scanner = LinuxWifiScanner('wlan0')
        mock = '''
        wlan0    Scan completed :
          Cell 01 - Address: 00:00:00:00:00:00
                    Channel:12
                    Frequency:2.467 GHz (Channel 12)
                    Quality=70/70  Signal level=-100 dBm  
                    Encryption key:on
                    ESSID:"AP1"
                    Bit Rates:1 Mb/s; 2 Mb/s; 5.5 Mb/s; 11 Mb/s
                    Bit Rates:6 Mb/s; 9 Mb/s; 12 Mb/s; 18 Mb/s; 24 Mb/s
                              36 Mb/s; 48 Mb/s; 54 Mb/s
                    Mode:Master
          Cell 02 - Address: 00:00:00:00:00:00
                    Channel:1
                    Frequency:2.412 GHz (Channel 1)
                    Quality=46/70  Signal level=-50 dBm  
                    Encryption key:on
                    ESSID:"AP2"
                    Bit Rates:1 Mb/s; 2 Mb/s; 5.5 Mb/s; 11 Mb/s; 9 Mb/s
                              18 Mb/s; 36 Mb/s; 54 Mb/s
                    Bit Rates:6 Mb/s; 12 Mb/s; 24 Mb/s; 48 Mb/s
                    Mode:Master     
        '''
        self._assert(scanner.parse(mock))

    def test_windows_wifi_scanner(self):
        scanner = WindowsWifiScanner()
        mock = '''
        SSID 1 : AP1
            Tipo di rete            : Infrastruttura
            Autenticazione          : WPA2-Personal
            Crittografia            : CCMP
            BSSID 1                 : 00:00:00:00:00:00
                 Segnale                 : 100%
                 Tipo frequenza radio    : 802.11g
                 Canale                  : 6
                 Velocità di base (Mbps) : 1 2 5.5 11
                 Altre velocità (Mbps) : 6 9 12 18 24 36 48 54
        
        SSID 2 : AP2
            Tipo di rete            : Infrastruttura
            Autenticazione          : WPA2-Personal
            Crittografia            : CCMP
            BSSID 1                 : 11:11:11:11:11:11
                 Segnale                 : 50%
                 Tipo frequenza radio    : 802.11n
                 Canale                  : 9
                 Velocità di base (Mbps) : 1 2 5.5 11
                 Altre velocità (Mbps) : 6 9 12 18 24 36 48 54
        '''

        self._assert(scanner.parse(mock))

    def _assert(self, scan):
        for ssid, rssi in scan.items():
            self.assertEqual(ssid, ssid.strip())
            self.assertIsInstance(rssi, int)

        self.assertIn('AP1', scan.keys())
        self.assertIn('AP2', scan.keys())
        self.assertEqual(abs(scan.get('AP1')), 100)
        self.assertEqual(abs(scan.get('AP2')), 50)
