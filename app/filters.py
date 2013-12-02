def _jinja2_filter_strftime(date, fmt='%Y-%b-%d %I:%M%p'):
    if date == None:
        return 'None'
    return date.strftime(fmt)

def init_app(app):
    """Initialize a flask application with custom filters"""
    app.jinja_env.filters['strftime'] = _jinja2_filter_strftime



