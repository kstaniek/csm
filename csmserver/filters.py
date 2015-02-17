import datetime
from jinja2 import Markup, evalcontextfilter, escape

def init(app):
    app.jinja_env.filters['elapsed_time'] = time_difference_UTC
    app.jinja_env.filters['datetime_string'] = get_datetime_string
    app.jinja_env.filters['beautify_platform'] = beautify_platform
    app.jinja_env.filters['none2blank'] = convert_none_to_blank
    
    # The nl2br filter uses the Jinja environment's context to determine
    # whether to autoescape
    app.jinja_env.filters['nl2br'] = evalcontextfilter(nl2br)
    app.jinja_env.filters['comma2br'] = evalcontextfilter(comma2br)


def convert_none_to_blank(value):
    if value == None:
        return ''  
    return value  

"""
Render newline \n characters as HTML line breaks <br />.
By default, HTML normalizes all whitespace on display. This filter allows
text with line breaks entered into a textarea input to later display in
HTML with line breaks.

The context argument is Jinja's state for template rendering, which
includes configuration. This filter inspects the context to determine
whether to auto-escape content, e.g. convert <script> to &lt;script&gt;.
"""    
def nl2br(context, value):
    formatted = u'<br />'.join(escape(value).split('\n'))
    if context.autoescape:
        formatted = Markup(formatted)
    return formatted

def comma2br(context, value):
    formatted = u'<br />'.join(escape(value).split(','))
    if context.autoescape:
        formatted = Markup(formatted)
    return formatted

def beautify_platform(platform):
    if platform is None:
        return 'Unknown'
    return platform.upper().replace('_','-')

def time_difference_UTC(otherdate):
    return humanize_date_difference(now = datetime.datetime.utcnow(), 
        otherdate = otherdate)
    
def humanize_date_difference(now, otherdate=None, offset=None):
    if otherdate is not None:
        dt = now - otherdate
        offset = dt.seconds + (abs(dt.days) * 60*60*24)
    else:
        return 'None'
    
    if offset:
        delta_s = int(offset % 60)
        offset /= 60
        delta_m = int(offset % 60)
        offset /= 60
        delta_h = int(offset % 24)
        offset /= 24
        delta_d = int(offset)
    else:
        #raise ValueError("Must supply otherdate or offset (from now)")
        return 'None'
 
    elapsed_time = ''
    
    if delta_d >= 1:
        elapsed_time += "{}d ".format(delta_d)
    if delta_h >= 1:
        elapsed_time += "{}h ".format(delta_h)
    if delta_m >= 1:
        elapsed_time += "{}m ".format(delta_m)
    if delta_s >= 1 and delta_d == 0:
        elapsed_time += "{}s ".format(delta_s)

    elapsed_time += 'ago'
    return elapsed_time
 
"""
Given a datetime object, return a human readable string (e.g 05/21/2014 11:12 AM)
"""
def get_datetime_string(datetime):
    try:
        if datetime is not None:
            return datetime.strftime("%m/%d/%Y %I:%M %p")
        return None
    except:
        return None
    
if __name__ == '__main__':
    otherdate = datetime.datetime.strptime('2014-10-02 17:13:24', "%Y-%m-%d %H:%M:%S")
    print(time_difference_UTC(otherdate))
