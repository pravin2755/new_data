from flask import request, Flask, render_template, make_response

app = Flask(__name__)


# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    # if request.method == 'POST':
    # user = request.form['nm']
    # resp = make_response(render_template('new.html'))
    resp = make_response("here is cookie ")
    resp.set_cookie('userID', "pravin")
    return resp


@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('userID')
    return '<h1>welcome ' + name + '</h1>'


@app.route('/count')
def count():
    # count1 = int(request.cookies.get('visit_cookie',0))
    getvalue=int(request.cookies.get("visit_cookie"))
    getvalue = getvalue + 1
    msg = "visited this page " + str(getvalue)
    resp = make_response(msg)
    resp.set_cookie("visit_cookie", str(getvalue))
    return resp


if __name__ == "__main__":
    app.run(debug=True, port=5002)
