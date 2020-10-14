#!/usr/bin/env python

class weatherCurrent:
    def __init__(self, dt, status, rain1h, sprinkler1h, clouds, weather_id, weather_type, weather_desc, \
    temperature, timeStamp_Sunrise, timeStamp_Sunset):
        self.dt = dt
        self.status = status
        self.rain1h = rain1h
        self.sprinkler1h = sprinkler1h
        self.clouds = clouds
        self.weather_id = weather_id
        self.weather_type = weather_type
        self.weather_desc = weather_desc
        self.temperature = temperature
        self.timeStamp_Sunrise = timeStamp_Sunrise
        self.timeStamp_Sunset = timeStamp_Sunset

    def printObject(self):
        print("______________________________________________________"+"\n")
        print("C U R R E N T"+"\n")
        print("dt: " + "\t" + "\t" + "\t"  + str(self.dt) +" UTX")
        print("status: " + "\t" + "\t" + str(self.status))
        print("rain1h: " + "\t" + "\t" + str(self.rain1h) +"mm")
        print("sprinkler1h: " + "\t" + "\t" + str(self.sprinkler1h) +"mm")
        print("clouds: " + "\t" + "\t" + str(self.clouds) + "%")
        print("weather_id: " + "\t" + "\t" + str(self.weather_id))
        print("weather_type: " + "\t" + "\t" + str(self.weather_type))
        print("weather_desc: " + "\t" + "\t" + str(self.weather_desc))
        print("temperature: " + "\t" + "\t" + str(self.temperature)+"°C")
        print("timeStamp_Sunrise: " + "\t"+ str(self.timeStamp_Sunrise)+ " UTX")
        print("timeStamp_Sunset: " + "\t"+ str(self.timeStamp_Sunset)+ " UTX")
        print("______________________________________________________"+"\n")

class weatherForecast:
    def __init__(self, dt, status, rain1h, clouds, weather_id, weather_type, weather_desc, \
    temperature):
        self.dt = dt
        self.status = status
        self.rain1h = rain1h
        self.clouds = clouds
        self.weather_id = weather_id
        self.weather_type = weather_type
        self.weather_desc = weather_desc
        self.temperature = temperature

    def printObject(self):
        print("______________________________________________________"+"\n")
        print("F O R E C A S T"+"\n")
        print("dt: " + "\t" + "\t" + "\t" + str(self.dt) +"UTX")
        print("status: " + "\t" + "\t" + str(self.status) +"mm")
        print("rain1h: " + "\t" + "\t" + str(self.rain1h) +"mm")
        print("clouds: " + "\t" + "\t" + str(self.clouds) + "%")
        print("weather_id: " + "\t" + "\t" + str(self.weather_id))
        print("weather_type: " + "\t" + "\t" + str(self.weather_type))
        print("weather_desc: " + "\t" + "\t" + str(self.weather_desc))
        print("temperature: " + "\t" + "\t" + str(self.temperature)+"°C")
        print("______________________________________________________"+"\n")
