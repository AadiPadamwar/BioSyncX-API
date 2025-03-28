from flask import Flask, request, jsonify
from database import connect_db
from datetime import datetime

app = Flask(__name__)


# Endpoint to store patient vitals
@app.route('/store_vitals', methods=['POST'])
def add_vitals():
    data = request.json  # Get JSON data from Android app
    user_id = data['user_id']
    heart_rate = data['heart_rate']
    temperature = data['temperature']
    blood_pressure = data['blood_pressure']
    oxygen_level = data['oxygen_level']

    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = """INSERT INTO Patient_Vitals (user_id, date, heart_rate, temperature, blood_pressure, oxygen_level) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (user_id, datetime.utcnow().date(), heart_rate, temperature, blood_pressure, oxygen_level)
        cursor.execute(sql, values)
        conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



# Endpoint to Fetch Latest Vitals for ML Model
@app.route('/get_latest_vitals/<int:user_id>', methods=['GET'])
def get_latest_vitals(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        sql = """SELECT * FROM Patient_Vitals WHERE user_id = %s ORDER BY date DESC LIMIT 1"""
        cursor.execute(sql, (user_id,))
        vitals = cursor.fetchone()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# Endpoint to Store ML Predictions
@app.route('/add_prediction', methods=['POST'])
def add_prediction():
    data = request.json
    user_id = data['user_id']
    vitals_id = data['vitals_id']
    prediction_result = data['prediction_result']

    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = """INSERT INTO Predictions (user_id, vitals_id, prediction_result) 
                     VALUES (%s, %s, %s)"""
        cursor.execute(sql, (user_id, vitals_id, prediction_result))
        conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# Endpoint to Fetch Predictions for a User
@app.route('/get_predictions/<int:user_id>', methods=['GET'])
def get_predictions(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        sql = """SELECT * FROM Predictions WHERE user_id = %s ORDER BY prediction_timestamp DESC"""
        cursor.execute(sql, (user_id,))
        predictions = cursor.fetchall()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


