#!/usr/bin/env python3
import ipdb

# Below line allows us to create instances of the flask app*
from flask import Flask
from flatburger.data import burgers
from flatburger.html import flatburger_html_code

# Crate a flask instance:
    # need to store it into a variable so it can be referenced
app = Flask(__name__)

# decorator starts with referencing the app -- we're about to make a route for our flask app
# route must start with a a /
@app.route('/')
# A view is the function that will determine what is shown
# function names don't really matter bc we never call them on flask
def index():
    return "<h1>Welcome to my Flask API!</h1>"

@app.route('/another_page')
def different_page():
    return f'<h1>This is another page!</h1>'

# Adding a parameter to a route
# can transform the route into a parameter with < >
# whatever follows the / is a parameter
# the value of that parameter gets stored in the route parameter
# this must be the same and the parameter in the view finder
@app.route('/intro/<name>')
def intro(name):
    # ipdb.set_trace()
    # print(name)
    return f"<h1>Hi! My name is {name}</h1>"

# Convert the datatype of a parameter
# add "int:" before the parameter to make it an integer
@app.route('/intro/<name>/<int:age>')
def intro_2(name, age):
    # ipdb.set_trace()
    return f"<h1>Hi! My name is {name}. I'm {age} years old.</h1>"


# Converting a parameter into a float
# the input must be the correct datatype
@app.route('/<float:number>')
def float_example(number):
    return f"<h1>The number is {number}</h1>"

# Deliverable #1 solution code
@app.route('/greeting/<first_name>/<last_name>')
def greeting(first_name, last_name):
    return f"<h1>Greetings, {first_name} {last_name}!</h1>"

# Deliverable #2 solution code
@app.route('/count_and_square/<int:number>')
def count_and_square(number):
    squared_nums_string = ""
    for num in range(1, number+1):
        squared_nums_string += f'{num ** 2}\n'
    return squared_nums_string
    # ipdb.set_trace()

# Delibverable #3 solution code
@app.route('/burgers')
def get_burgers():
    return burgers

# Deliver #4 solution code
@app.route('/flatburger_page')
def flatburger():
    return flatburger_html_code


if __name__ == "__main__":
    app.run(port=7777, debug=True)