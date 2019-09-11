from flask import Flask, request

app = Flask(__name__)


def calculate(total, trucks):
    response = "{}{}".format(total,trucks)
    return response


@app.route('/')
def get_ratio():
    data = request.get_json()
    return calculate(data['total'], data['trucks'])
