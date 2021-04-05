# Python Indoor Positioning library

This library aims to provide a hardware-independent system for indoor positioning.
Hardware-independent means that you can either use WiFi, Bluetooth, or any other wireless technology you prefer.

The indoor positioning process involves 2 steps:

 1. collect data to train Machine Learning model
 2. use the model to predict where you're in
 
**NOTICE: this library works by classifying the location you're in: it can't estimate your coordinates in a room**

## How to use

First of all, you want to collect a few samples of the access points in the locations you want to recognize.

```python
from indoorpositioning import IndoorPositioning
from indoorpositioning.scanner import LinuxWifiScanner


positioning = IndoorPositioning(scanner=LinuxWifiScanner('wlan0'))
positioning.collect()
```

The `collect()` function will start an interactive process where you're asked to input a location and how many scans you want to perform:
move a bit around the room and let the scan complete. Then move to the next room and repeat until you're done. 

Now you can train a Machine Learning model to classify the location based on the collected data.

```python
from sklearn.tree import DecisionTreeClassifier


clf = positioning.fit(DecisionTreeClassifier())
print('Score on train dataset: %2.f' % clf.score(positioning.X, positioning.y))
```

`positioning.X` and `positioning.y` return the formatted X and y arrays you need to train a classifier from the `sklearn` package.

Now you can run the classifier around you're house / office / whatever and get the predicted location.

```python
while True:
    print('You are in', positioning.predict_location(clf))
```

## ToDo

 - [x] Linux Wifi scanner
 - [x] OS X Wifi scanner
 - [x] Windows Wifi scanner
 - [ ] Linux Bluetooth scanner
 - [ ] OS X Bluetooth scanner
 - [ ] Windows Bluetooth scanner
 - [ ] Other wireless technologies?