def _get_wind_direction(wind_deg: int) -> str:
    if 337.5 <= wind_deg < 360 or 0 <= wind_deg < 22.5:
        return "северный"
    elif 22.5 <= wind_deg < 67.5:
        return "северо-восточный"
    elif 67.5 <= wind_deg < 112.5:
        return "восточный"
    elif 112.5 <= wind_deg < 157.5:
        return "юго-восточный"
    elif 157.5 <= wind_deg < 202.5:
        return "южный"
    elif 202.5 <= wind_deg < 247.5:
        return "юго-западный"
    elif 247.5 <= wind_deg < 292.5:
        return "западный"
    elif 292.5 <= wind_deg < 337.5:
        return "северо-западный"
    else:
        return "нет данных"
