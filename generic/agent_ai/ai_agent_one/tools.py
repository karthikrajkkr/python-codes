def get_weather(city):
    """Assume this tool calls an external API and returns the accurate Weather.
    Currently, it is simply hardcoded..."""
    weather = {'halifax':'sunny', 'montreal':'rainy', 'toronto':'cloudy'}
    return weather[city.lower()]