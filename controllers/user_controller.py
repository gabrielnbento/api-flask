from flask import Flask, Response, Request
import json
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
df = pd.read_csv('./dataframes/users.csv')

@app.route('/users', methods=['GET'])
def all_users():
    response_data = json.dumps(df.to_dict('records'), ensure_ascii=False)
    return Response(response_data, mimetype='application/json; charset=utf-8')
@app.route('/user/login/<email>&<password>', methods=['GET'])
def get_user(email, password):
    user = df.loc[(df['email'] == email) & (df['password'] == password)]
    user_data = user.to_dict('records')

    if user_data:
        response_data = json.dumps(user_data[0], ensure_ascii=False)
  
        return Response(response_data, mimetype='application/json; charset=utf-8')
    else:
        response_data = json.dumps({'error': 'User nao encontrado'}, ensure_ascii=False)
        return Response(response_data, mimetype='application/json; charset=utf-8', status=404)
    
@app.route('/user/register', methods=['POST'])
def reigster_user():
    data = Request.get_json()

    new_user ={
        'user_id': df['user_id'].max() + 1,
        'user_name': data['name'],
        'email': data['email'],
        'password': data['password']
    }

    df = df.append(new_user, ignore_index=True)

    df.to_csv('./dataframes/users.csv', index=False)

    return Response(json.dumps({'message': 'User criado com sucesso'}), mimetype='application/json; charset=utf-8')

if __name__ == '__main__':
    app.run(debug=True)
