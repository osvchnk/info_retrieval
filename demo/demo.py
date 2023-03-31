from flask import Flask, render_template, request
from demo.search import search

app = Flask(__name__, template_folder="templates")


@app.route("/", methods=['GET', 'POST'])
def hello_world():

    if request.method == 'POST':
        result = search(request.values.get("data"))
        return result

        # return search(request.form['input_value'])
    return render_template('main.html')
