class temperatureChange:
    def temperatureCelcius(x):
        return (x-32)  * (5/9)
    #end function
    def temperatureFarenheit(x):
        return (x * (9/5)) + 32
    #end function
#end class

questionFarenheit = input("\nCan you tell me today's temperature in degrees Farenheit? (Y/N)")
if questionFarenheit == "y" or questionFarenheit == "Y":
    userFarenheit = int(input("Tell me the temperature in degrees Farenheit: "))
    celcius = temperatureChange.temperatureCelcius(userFarenheit)
    print ("Today's temperature in degrees Celsius is", celcius)
else:
    print ("That's to bad. Invest in a thermometer.")
#end if

questionCelsius = input("\nCan you tell me today's temperature in degrees Celsius? (Y/N)")
if questionCelsius == "y" or questionCelsius == "Y":
    userCelsius = int(input("Tell me the temperature in degrees Celcius: "))
    farenheit = temperatureChange.temperatureFarenheit(userCelsius)
    print ("Today's temperature in degrees Farenheit is", farenheit)
else:
    print ("That's to bad. Invest in a thermometer.")
#end if
#end program
