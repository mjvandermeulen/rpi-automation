#!/usr/bin/env python

import os
import glob
from time import time  # for plotting

import matplotlib.pyplot as plt

import automation_classes.temperature_reader as temperature_reader


class Temperature (object):
    """
    This class:
    - FOR NOW ALL IN FAHRENHEIT. otherwise it'll get messed up.
    - reads the temperature
    - remembers the previously read temperatures in a list.
    - calculates the throttle needed to reach set temperature (from -1 to 1)
    - has a method for plotting.

    Attributes
    ----------
    interval: int
        time in seconds between readings (not enforced, since timing is up to the caller of the class methods)
    current_temp_f: float
        current (last read) temperature in Fahrenheit
    current_temp_c: float
        current (last read) temperature in Celsius
    throttle: float
        throttle needed to reach the set temperature from -1 to 1

    Methods
    -------
    read_temp_f(): float
        reads the temperature and stores this data.
        Triggers recalculation of the throttle.
        returns the read temperature

    plot()
        plots the list data.

    write_to_csv_file(filename = "temperature")
        writes to "[temperature] [timestamp].csv"
        e.g.: "temperature 2019 01 21 18:27.csv"
        creates this file if it does not exist.
        writes the following columns:
        HEADER?
        - temperature in fahrenheit
        - throttle
        - p proportion(al)
        - i integral
        - d derivative
    """

    def __init__(self, target_temp, interval):  # TODO: refactor to allow for celsius
        """ 
        initializes temperature object.
        NOTE: does not need the filename, this needs to be given everytime the write() method is called.

        Parameters
        ----------
        target_temp : int
            target temperature in Fahrenheit
        interval : int, optional
            time in seconds between readings (the default is 60, which [default_description])

        """

        self.target_temp = target_temp
        self.interval = interval

        self.current_temp_f = 1000
        self.throttle = -1

        # current data
        self._integral = 0

        # past (and current) data
        self._time_list = []
        self._t_list = []
        # self._p_list = []
        # self._i_list = []
        # self._d_list = []

        # plotting
        plt.ion()  # interactive on

        self._temp_reader = temperature_reader.TemperatureReader()

    def _calculate_throttle(self, t):
        print("set throttle to -1 if temp too high, or 1 if too low")
        if t < self.target_temp:
            return 1
        return -1

    def read_temp_f(self):
        t = self._temp_reader.read_temp_f()
        self._t_list.append(t)
        self._time_list.append(time())
        self.current_temp_f = t
        self.throttle = self._calculate_throttle(t)
        return t

    def plot(self):
        """
        plot the current data (not data from a file)
        """
        for t in self._t_list:
            print("t: {:5.2f} fahrenheit".format(t))
        plt.clf()
        plt.scatter(self._time_list, self._t_list)
        plt.plot(self._time_list, self._t_list)
        # plt.show(block=True)# block=True only needed if plt.ion()
        plt.pause(.001)
        plt.show()  # plt.draw() in instructions.
