#!/usr/bin/env python

class weatherClass:
    def __init__(self, rain1h, clouds, weather_id, weather_type, weather_desc, \
    temperature, timeStamp_DataLoad, timeStamp_Sunrise, timeStamp_Sunset):
        self.rain1h = rain1h
        self.clouds = clouds
        self.weather_id = weather_id
        self.weather_type = weather_type
        self.weather_desc = weather_desc
        self.temperature = temperature
        self.timeStamp_DataLoad = timeStamp_DataLoad
        self.timeStamp_Sunrise = timeStamp_Sunrise
        self.timeStamp_Sunset = timeStamp_Sunset

    def printObject(self):
        print("rain1h: " + "\t" + "\t" + str(self.rain1h))
        print("clouds: " + "\t" + "\t" + str(self.clouds))
        print("weather_id: " + "\t" + "\t" + str(self.weather_id))
        print("weather_type: " + "\t" + "\t" + str(self.weather_type))
        print("weather_desc: " + "\t" + "\t" + str(self.weather_desc))
        print("temperature: " + "\t" + "\t" + str(self.temperature))
        print("timeStamp_DataLoad: " + "\t" + str(self.timeStamp_DataLoad))
        print("timeStamp_Sunrise: " + "\t" + str(self.timeStamp_Sunrise))
        print("timeStamp_Sunset: " + "\t" + str(self.timeStamp_Sunset))
