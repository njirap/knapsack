from flask import Flask, request

app = Flask(__name__)


def calculate(tonnes, ratios, index):
    ratios[index][1] = ratios[index][1] + tonnes // ratios[index][0]
    remainder = tonnes % ratios[index][0]
    if remainder == 0:
        return ratios
    else:
        for item in ratios[:index][::-1]:
            if remainder % item[0] == 0:
                item[1] = remainder // item[0]
                return ratios
        for item in ratios[:index][::-1]:
            if remainder // item[0] > 0:
                item[1] = remainder // item[0]
                remainder = remainder % item[0]
                for item2 in ratios[:index-1][::-1]:
                    if remainder % item2[0] == 0:
                        item2[1] = remainder // item2[0]
                        return ratios
                if len(ratios[:index-1]) == 0:
                    response = "Perfect distribution not possible\n"
                    response = response + "Ratios: {}, Uncarried balance: {}".format(ratios, remainder)
                    return response
                if ratios[index][1] < 2:
                    remainder = remainder + ratios[index+1][0]
                    ratios[index+1][1] -= 1
                else:
                    remainder = remainder + ratios[index][0]
                    ratios[index][1] -= 1
                    index -= 1
                calculate(remainder, ratios, index)
                return ratios

@app.route('/')
def get_ratio():
    data = request.get_json()
    if data['total'] < min(data['trucks']):
        return "Cargo too small"
    data['trucks'].sort()
    ratios = [[x, 0] for x in data['trucks']]
    return "{}".format(calculate(data['total'], ratios, -1))
