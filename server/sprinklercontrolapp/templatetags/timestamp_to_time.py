from django import template    
register = template.Library()  

@register.filter('timestamp_to_time')
def convert_timestamp_to_time(timestamp):
    import time, datetime
    return datetime.datetime.fromtimestamp(int(timestamp))