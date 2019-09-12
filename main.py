from flask import Flask, request

app = Flask(__name__)


def calculate(total, trucks):
    response = "{}{}".format(total,trucks)
    return response


@app.route('/')
def get_ratio():
    data = request.get_json()
    if data['total'] < min(data['trucks']):
        return "Cargo too small"
    return calculate(data['total'], data['trucks'])
