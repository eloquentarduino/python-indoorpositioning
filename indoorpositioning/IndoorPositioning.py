import json
from random import shuffle
from indoorpositioning.scanner.BaseScanner import BaseScanner


class IndoorPositioning:
    """
    Hardware-independent indoor positioning system
    """
    def __init__(self, scanner, preload_scans=None):
        """
        Constructor
        :param scanner: BaseScanner
        :param preload_scans: dict load results from previous scans
        """
        assert isinstance(scanner, BaseScanner), 'scanner MUST be an instance of BaseScanner'
        assert preload_scans is None or isinstance(preload_scans, dict), 'preload_scans MUST be None or a dict'

        self.scanner = scanner
        self.scans = preload_scans or {}

    @property
    def access_points(self):
        """
        Get list of known access points
        :return:
        """
        scans = [scan for location_scans in self.scans.values() for scan in location_scans]
        ssids = [ssid for scan in scans for ssid in scan.keys()]

        return sorted(list(set(ssids)))

    @property
    def X(self):
        """
        Get X array
        :return: list
        """
        Xs = [[self.to_array(scan) for scan in location_scans] for location_scans in self.scans.values()]

        return [x for X in Xs for x in X]

    @property
    def y(self):
        """
        Get y array
        :return: list
        """
        ys = [[i] * len(location_scans) for i, location_scans in enumerate(self.scans.values())]

        return [y for Y in ys for y in Y]

    @property
    def classmap(self):
        """
        Get classmap
        :return: dict
        """
        return {i: ssid for i, ssid in enumerate(self.scans.keys())}

    def knows_ssid(self, ssid):
        """
        Test if given SSID is known
        :param ssid: str
        :return: bool
        """
        try:
            return self.access_points.index(ssid) >= 0
        except ValueError:
            return False

    def scan(self):
        """
        Scan for access points
        :return: dict
        """
        return self.scanner.scan()

    def scan_location(self, location_name, repeat=5, override=False):
        """
        Scan a location a given number of times
        :param location_name: str
        :param repeat: int
        :param override: bool
        :return:
        """
        assert len(location_name) > 0, 'location_name MUST be a non-empty string'
        assert repeat > 0, 'repeat MUST be a positive number'

        if override:
            self.scans[location_name] = []
        else:
            self.scans.setdefault(location_name, [])

        for i in range(repeat):
            print('scanning %d/%d' % (i + 1, repeat))
            scan = self.scan()
            print('%d access points found' % len(scan))
            self.scans[location_name].append(scan)

    def scan_features(self):
        """
        Scan access points and transform to features
        :return: array
        """
        return self.to_array(self.scan())

    def to_array(self, scan):
        """
        Convert scan results to features
        :param scan: dict
        :return: array
        """
        valid_access_points = {ssid: rssi for ssid, rssi in scan.items() if self.knows_ssid(ssid)}
        known_access_points = self.access_points

        return [valid_access_points.get(ssid, 0) for ssid in known_access_points]

    def save_to(self, filename):
        """
        Save data to file
        :param filename: str
        :return:
        """
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.scans, file)

    def load_from(self, filename, merge=True):
        """
        Load data from file
        :param filename: str
        :param merge: bool
        :return:
        """
        with open(filename, encoding='utf-8') as file:
            data = json.load(file)

            if merge:
                for location_name, location_scans in data.items():
                    self.scans.setdefault(location_name, [])
                    self.scans[location_name] += location_scans

            else:
                self.scans = data

    def collect(self):
        """
        Collect training data
        :return:
        """
        # before scanning, be sure we can store the results somewhere
        filename = input('Where are you going to store your results? ').strip()

        with open(filename, 'w'):
            pass

        # perform scan in all the locations
        while True:
            location_name = input('Which location are you going to scan? (leave empty to stop): ').strip()

            if location_name == '':
                break

            repeat = int(input('How many scans do you want to perform? ').strip())
            self.scan_location(location_name, repeat=repeat)

        self.save_to(filename)
        print('Done, you now have a dataset to train a machine learning model using the fit(clf) method')

    def fit(self, clf):
        """
        Train a classifier
        :param clf:
        :return:
        """
        xy = list(zip(self.X, self.y))
        shuffle(xy)
        X, y = zip(*xy)

        clf.fit(X, y)

        return clf
