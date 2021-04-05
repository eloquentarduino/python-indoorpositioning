from unittest import TestCase
from indoorpositioning import IndoorPositioning
from indoorpositioning.scanner import OSXWifiScanner


class TestIndoorPositioning(TestCase):
    def test_scan(self):
        scanner = OSXWifiScanner()
        positioning = IndoorPositioning(scanner=scanner)

        for ssid, rssi in positioning.scan().items():
            self.assertEqual(ssid, ssid.strip())
            self.assertIsInstance(rssi, int)

    def test_access_points(self):
        scanner = OSXWifiScanner()
        scans = {
            'test': [{'ap1': 1, 'ap2': 2}]
        }
        positioning = IndoorPositioning(scanner=scanner, preload_scans=scans)

        self.assertEqual(positioning.access_points, ['ap1', 'ap2'])

    def test_to_array(self):
        scanner = OSXWifiScanner()
        scans = {
            'test': [{'ap1': 1, 'ap2': 2}]
        }
        positioning = IndoorPositioning(scanner=scanner, preload_scans=scans)
        scan1 = {'ap1': 1}
        scan2 = {'ap2': 2}
        scan3 = {'ap3': 3}

        self.assertEqual(positioning.to_array(scan1), [1, 0])
        self.assertEqual(positioning.to_array(scan2), [0, 2])
        self.assertEqual(positioning.to_array(scan3), [0, 0])

    def test_Xy(self):
        scanner = OSXWifiScanner()
        scans = {
            'test0': [{'ap1': 1, 'ap2': 2}],
            'test1': [{'ap1': 1, 'ap3': 3}],
            'test2': [{'ap2': 2, 'ap3': 3}],
        }
        positioning = IndoorPositioning(scanner=scanner, preload_scans=scans)

        self.assertEqual(positioning.X, [[1, 2, 0], [1, 0, 3], [0, 2, 3]])
        self.assertEqual(positioning.y, [0, 1, 2])
        self.assertEqual(positioning.classmap, {0: 'test0', 1: 'test1', 2: 'test2'})

    def test_save_load(self):
        scanner = OSXWifiScanner()
        scans = {
            'test0': [{'ap1': 1, 'ap2': 2}],
            'test1': [{'ap1': 1, 'ap3': 3}],
            'test2': [{'ap2': 2, 'ap3': 3}],
        }

        # save
        positioning = IndoorPositioning(scanner=scanner, preload_scans=scans)
        positioning.save_to('indoorpositioning/tests/data/positioning.json')

        # load
        positioning = IndoorPositioning(scanner=scanner)
        positioning.load_from('indoorpositioning/tests/data/positioning.json')

        self.assertEqual(positioning.access_points, ['ap1', 'ap2', 'ap3'])

        # load + merge
        positioning = IndoorPositioning(scanner=scanner, preload_scans={'test0': [{'ap4': 4}]})
        positioning.load_from('indoorpositioning/tests/data/positioning.json')

        self.assertEqual(positioning.access_points, ['ap1', 'ap2', 'ap3', 'ap4'])
        self.assertEqual(positioning.y, [0, 0, 1, 2])
