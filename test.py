import predict
import pandas as pd
import requests

#Test1
# sub = {
#     "msno" : 're3gtxre54yh5r4y66uyr61u2',
#     "city" : '1',
#     "gender" : 2.0,
#     "registered_via" : '1.0',
#     "registration_init_time" : 20191115.0,
#     "date" : '20191115.0',
#     "num_25" : 2.0,
#     "num_50" : 0.0,
#     "num_75" : 1.0,
#     "num_985" : 1.0,
#     "num_100" : 1.0,
#     "num_unq" : 5.0,
#     "total_secs" : 10
# }

#Test2
sub = {
    # "msno" : 're3gtxre54yh5r4y66uyr54s3',
    "city" : '13',
    "gender" : 2.0,
    "registered_via" : '7.0',
    "registration_init_time" : 20161115.0,
    # "date" : '20151115.0',
    "num_25" : 0.0,
    "num_50" : 0.0,
    "num_75" : 0.0,
    "num_985" : 0.0,
    "num_100" : 0.0,
    "num_unq" : 0.0,
    "total_secs" : 10
}


url = 'http://127.0.0.1:9696/predict'
response = requests.post(url, json=sub)
print(response.json())

# pred = predict.predict(sub)
# print(pred)