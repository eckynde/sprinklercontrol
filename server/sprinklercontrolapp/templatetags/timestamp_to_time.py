from django import template    
register = template.Library()  

# Implementating of a template tag; Transforms a timestamp field to a datetime field for the usage of django template tags
@register.filter('timestamp_to_time')
def convert_timestamp_to_time(timestamp):
    import time, datetime
    return datetime.datetime.fromtimestamp(int(timestamp))