import pickle
from flask import Flask, request, jsonify

with open('models/preproccesor.bin', 'rb') as f_in:
    dv = pickle.load(f_in)

with open('models/DecisionTreeClassifier.bin', 'rb') as f_in:
    model = pickle.load(f_in)
    print(type(model))


def predict(sub):
    X = dv.transform(sub)
    preds = model.predict(X)

    return bool(preds[0])

app = Flask('churn_prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    sub = request.get_json()
    pred = predict(sub)

    result = {
        'result' : pred
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
