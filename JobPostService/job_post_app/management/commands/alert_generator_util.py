def format_location(location_dict):
    return '{0}, {1}, {2}, {3}'.format(location_dict['streetAddress'], location_dict['city'], location_dict['state'],
                                       location_dict['zipCode'])


GOOGLE_MAP_URL_PREFIX = 'https://www.google.com/maps/place/'


def get_location_link(location_str):
    return GOOGLE_MAP_URL_PREFIX + location_str