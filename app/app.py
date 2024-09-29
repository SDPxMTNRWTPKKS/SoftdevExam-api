from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "ExamSoftdev Success!!!!!"

@app.route('/is_prime/<x>',methods=['GET'])
def show_number(x):

    x = int(x)

    if x <= 1:
        return 'False'
    
    for i in range(2, int(x**0.5) + 1):
        if x % i == 0:
            return 'False'
    
    return 'True'

if __name__ == '__main__':
    app.run(debug=True)
