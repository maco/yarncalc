from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/calculate', methods=['GET'])
def calc():
    length = request.args.get('length', '')
    lunit = request.args.get('lengthunit', '')
    weight = request.args.get('weight', '')
    wunit = request.args.get('weightunit', '')
    fiber = request.args.get('fiber', '')
    plies = request.args.get('plies', '')
    
    pounds = to_pounds(weight,wunit)
    hanks = to_hanks(length, lunit, fiber)

    hanks_per_pound = float(hanks) / float(pounds)
    size = int(float(hanks_per_pound) * int(plies))
    if fiber == "wool":
        size_formatted = str(plies)+"/"+str(size)
    else:
        size_formatted = str(size)+"/"+str(plies)

    return render_template('result.html', size=size_formatted)

def to_pounds(weight, unit):
    if unit == "lb":
        pounds = weight
    elif unit == "oz":
        pounds = float(weight) / 16
    elif unit == "kg":
        pounds = float(weight) * 2.2
    else: # grams
        pounds = float(weight) * 2.2 *.001

    return pounds

def to_hanks(length, unit, fiber):
    yards_per_hank = {
        'cotton': 840,
        'linen': 300,
        'silk': 840,
        'wool': 560
    }

    if unit == "yd":
        yards = length
    elif unit == "m":
        yards = float(length) * 1.093

    hanks = float(yards) / float(yards_per_hank[fiber])
    return hanks

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
