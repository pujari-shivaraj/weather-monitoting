def kelvin_to_celsius(kelvin_temp):
    return round(kelvin_temp - 273.15, 2)

def kelvin_to_fahrenheit(kelvin_temp):
    return round((kelvin_temp - 273.15) * 9/5 + 32, 2)

def convert_temperature(temp_kelvin):
    from app.config import Config
    if Config.TEMP_UNIT == "Fahrenheit":
        return kelvin_to_fahrenheit(temp_kelvin)
    return kelvin_to_celsius(temp_kelvin)
