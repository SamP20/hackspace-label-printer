from flask import Flask, render_template, request, abort
from print import print_label

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/print')
def print():
    your_name = request.args.get("your_name")
    label_type = request.args.get("label_type")
    if label_type not in ["short_stay", "long_stay"]:
        abort(400)
    print_label(your_name, label_type)
    return render_template("print.html", your_name=your_name, label_type=label_type)

if __name__ == '__main__':
    app.run(debug=True)