from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Is odd number"

@app.route('/isodd/<x>',methods=['GET'])
def show_number(x):

    x = int(x)

    if x%2 == 0:
        return 'False'
    else :
        return 'True'

if __name__ == '__main__':
    app.run(debug=True)
