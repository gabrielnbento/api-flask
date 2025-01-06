from flask import Flask, Response
import json
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
df = pd.read_csv('./dataframes/tickets.csv')

@app.route('/')
def index():
    return '{"message": "Hello World"}'

@app.route('/all-tickets', methods=['GET'])
def all_tickets():
    response_data = json.dumps(df.to_dict('records'), ensure_ascii=False)
    return Response(response_data, mimetype='application/json; charset=utf-8')

@app.route('/ticket/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = df.where(df['Numero_do_Voo'] == ticket_id).dropna()
    ticket_data = ticket.to_dict('records')

    if ticket_data:
        response_data = json.dumps(ticket_data[0], ensure_ascii=False)
  
        return Response(response_data, mimetype='application/json; charset=utf-8')
    else:
        response_data = json.dumps({'error': 'Ticket não encontrado'}, ensure_ascii=False)
        return Response(response_data, mimetype='application/json; charset=utf-8', status=404)

if __name__ == '__main__':
    app.run(debug=True)
