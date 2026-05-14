def get_average_rainfall(data, location):

    location_data = data[data["SUBDIVISION"] == location]

    if location_data.empty:
        return 1000

    return location_data["ANNUAL"].mean()