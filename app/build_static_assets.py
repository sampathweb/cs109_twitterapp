from webassets import Environment, Bundle

my_env = Environment('static/', 'static/')


common_css = Bundle(
    'css/vendor/normalize.css',
    'css/vendor/foundation.css',
    'css/app.css',
    output='public/css/common.css'
    )

common_js = Bundle(
    'js/vendor/jquery.min.js',
    'js/vendor/custom.modernizr.js',
    'js/vendor/foundation.min.js',
    'js/vendor/d3.v3.js',
    'js/app.js',
    output='public/js/common.js'
    )

my_env.register('css_all', common_css)
my_env.register('js_all', common_js)

my_env['css_all'].urls()
my_env['js_all'].urls()
