from flask import Flask, request

app = Flask(__name__)


def calculate(tonnes, ratios, index):
        # check if it perfectly fits in 1 truck type
    i = index
    for item in ratios[index:]:
        if tonnes % item[0] == 0:
            ratios[i][1] = ratios[i][1] + tonnes // ratios[i][0]
            return ratios
        i += 1

    # fill largest truck
    ratios[index][1] = ratios[index][1] + tonnes // ratios[index][0]

    # take remainder after filling largest truck
    remainder = tonnes % ratios[index][0]
    for item in ratios[index+1:]:
        if remainder % item[0] == 0:
            item[1] = remainder // item[0]
            return ratios
    i = 1
    for item in ratios[index+i:]:
        if remainder // item[0] > 0:
            item[1] = remainder // item[0]
            remainder2 = remainder % item[0]
            if item == ratios[-1]:
                response = "Complete distribution not possible\n"
                response = response + "Ratios: {}\nUncarried balance: {}".format(ratios, remainder2)
                return response
            for item2 in ratios[index+i:]:
                if remainder2 % item2[0] == 0:
                    item2[1] = remainder2 // item2[0]
                    return ratios
            if ratios[index+i][1] < 2:
                remainder = remainder + ratios[index+1][0]
                ratios[index+1][1] -= 1
            else:
                remainder = remainder + ratios[index][0]
                ratios[index][1] -= 1
                index -= 1
            calculate(remainder, ratios, index)
            return ratios
        else:
            i += 1

@app.route('/')
def get_ratio():
    data = request.get_json()

    # Edge cases
    if data is None:
        return "Pass the parameters in the form\n{'total':90, 'trucks': [56, 23, 45]}"

    if (not 'total' in data) or (not 'trucks' in data):
        return "Pass both required parameters in the form\n{'total':90, 'trucks': [56, 23, 45]}"

    if data['total'] < min(data['trucks']):
        return "Cargo too small"
    # End of edge cases

    data['trucks'].sort()
    trucks = data['trucks'][::-1]
    index = 0
    if trucks[0] > data['total']:
        for truck in trucks[1:]:
            index += 1
            if truck < data['total']:
                break
    ratios = [[x, 0] for x in trucks]
    return "{}".format(calculate(data['total'], ratios, index))
