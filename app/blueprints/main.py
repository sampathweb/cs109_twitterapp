from flask import Blueprint, render_template, session, redirect, url_for, request, abort
from flask import current_app, make_response

main = Blueprint(
    'main', 
    __name__,
    template_folder='templates'
)

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')

@main.route('/about/', methods=['GET', 'POST'])
def about():
    return render_template('main/about.html')

@main.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'))


@main.route("/simple.png")
def simple():
    import datetime
    import StringIO
    import random
 
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
 
    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response
