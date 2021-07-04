from flask import Flask, make_response

from data.input import load_input_data
from voting.stv import rank_stv, LOG_FILE

app = Flask(__name__)


@app.route('/rank/', methods=['GET'])
def return_rank():
    df = load_input_data()
    ranking = rank_stv(df)
    return ranking.to_html()


@app.route('/steps/', methods=['GET'])
def return_steps():
    df = load_input_data()
    ranking = rank_stv(df, log=True)
    with open(LOG_FILE, 'r') as file:
        steps = file.read()
        print(steps)
    response = make_response(steps, 200)
    response.mimetype = "text/plain"
    return response


@app.route('/')
def index():
    return "<h1>Pub Wednesday Democracybot</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
