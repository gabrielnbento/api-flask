from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
df = pd.read_csv('tickets.csv')
@app.route('/')
def index():
    return jsonify({'message': 'Hello World'})

@app.route('/all-tickets', methods=['GET'])
def all_tickets():
    return jsonify(df.to_dict())

@app.route('/ticket/<string:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = df.where(df['Numero_do_Voo'] == ticket_id).dropna()
    return jsonify(ticket.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
