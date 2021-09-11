from flask import Flask, jsonify, request, render_template
from datatools import *
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})



jsn=[]


@app.route('/search/<s>', methods=['GET', 'POST','SEARCH'])
def search(s): 

        
        
        print("searching "+s)

        res=searchApi(s)
        print('Incoming..')
        return jsonify(res)

@app.route('/category/<cat>' ,methods=['GET', 'POST'])

def category(cat):
    print(cat)
    return jsonify(getCategory(cat))

@app.route('/prods/' ,methods=['GET', 'POST'])

def prods():
    return jsonify(getallprods())
    






@app.route('/test')
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('index.html')
    

if __name__ == "__main__":
    app.run()