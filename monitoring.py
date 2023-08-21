import pandas as pd
import mlflow
import random
import pickle

from evidently import ColumnMapping
from evidently.report import Report
from eveidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric

from joblib import load, dump
from tqdm import tqdm

from prefect import flow, task
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from prefect.task_runners import SequentialTaskRunner

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from lightgbm import LGBMClassifier

from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score

@task(name="read_data")
def read_data(filepath):
    #<h4> dataset train </h4>
    df_train_dataset = pd.read_csv(f'{filepath}/train.csv')

    #<h4> dataset members</h4>
    df_members_v3 = pd.read_csv(f'{filepath}/members_v3.csv')

    #<h4> dataset user_logs </h4>
    df_user_logs_v2 = pd.read_csv(f'{filepath}/user_logs_v2.csv')

    return df_train_dataset, df_members_v3, df_user_logs_v2

@task(name="merge")
def merge(df1,df2):

    df_train = df1.merge(df2, how='left', on='msno')

    return df_train

@task(name="pre_merge_processing")
def pre_merge_processing(df_train_dataset, df_members_v3, df_user_logs_v2):

    #fill null values with 'ns' for non-specified
    df_members_v3['gender'].fillna('ns', inplace=True)
    df_members_v3['city'].fillna(0, inplace=True)

    #dropping bd (birthday/age) as it has a weird range from -ve to +ve
    df_members_v3.drop(['bd'], axis=1, inplace=True)

    #convert gender to int value

    gender = {'male':1, 'female':2, 'ns':0}
    df_members_v3['gender'] = df_members_v3['gender'].map(gender)


    df_user_logs_v2['date'] = df_user_logs_v2['date'].astype(str).str.slice(0,6)
    df_user_logs_v2_agg = df_user_logs_v2.groupby(['msno', 'date']).agg({'num_25': 'mean'
                                             , 'num_50': 'mean'
                                             , 'num_75': 'mean'
                                             , 'num_985': 'mean'
                                             , 'num_100': 'mean'
                                             , 'num_unq': 'sum'
                                             , 'total_secs': 'sum'}).reset_index()


    return df_train_dataset, df_members_v3, df_user_logs_v2

@task(name="post_merge_processing")
def post_merge_processing(df_train):

    # replacing categorical variables null values with "ns" for non-specified
    df_train['gender'].fillna(0, inplace=True)
    df_train['city'].fillna('ns', inplace=True)
    # df_train['bd'].fillna('ns', inplace=True)
    df_train['registered_via'].fillna('ns', inplace=True)

    # replacing numerical variables null values with "0" assuming no usage
    df_train['num_25'].fillna(0, inplace=True)
    df_train['num_50'].fillna(0, inplace=True)
    df_train['num_75'].fillna(0, inplace=True)
    df_train['num_985'].fillna(0, inplace=True)
    df_train['num_100'].fillna(0, inplace=True)
    df_train['num_unq'].fillna(0, inplace=True)
    df_train['total_secs'].fillna(0, inplace=True)
    df_train['registration_init_time'].fillna(0, inplace=True) #considering registration time to be epoch 0

    return df_train

@task(name="split_data")
def split_data(df_train):

    df_full = df_train

    df_full_train, df_test = train_test_split(df_full, test_size=0.2, random_state=42)
    df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=42)
    df_train = df_train.reset_index(drop=True)
    df_val = df_val.reset_index(drop=True)
    df_test = df_test.reset_index(drop=True)

    y_train = df_train.is_churn.values
    y_val = df_val.is_churn.values
    y_test = df_test.is_churn.values

    del df_train['is_churn']
    del df_val['is_churn']
    del df_test['is_churn']

    return df_full, df_train, df_val, df_test, y_train, y_val, y_test

@task(name="save_pickle_dataset")
def save_pickle_dataset(df_full, df_train, df_val, df_test, y_train, y_val, y_test):
    y_train = pd.DataFrame(y_train)
    y_val = pd.DataFrame(y_val)
    y_test = pd.DataFrame(y_test)

    df_full.to_pickle("./df_full.pkl")
    df_train.to_pickle("./df_train.pkl")
    df_val.to_pickle("./df_val.pkl")
    df_test.to_pickle("./df_test.pkl")

    y_train.to_pickle("./y_train.pkl")
    y_val.to_pickle("./y_val.pkl")
    y_test.to_pickle("./y_test.pkl")

@task(name="read_pickle_dataset")
def read_pickle_dataset():
    # <h3> Read Pickled dataframees </h3>
    df_full = pd.read_pickle("./df_full.pkl")
    df_train = pd.read_pickle("./df_train.pkl")
    df_val = pd.read_pickle("./df_val.pkl")
    df_test = pd.read_pickle("./df_test.pkl")

    y_train = pd.read_pickle("./y_train.pkl")
    y_val = pd.read_pickle("./y_val.pkl")
    y_test = pd.read_pickle("./y_test.pkl")

    return df_full, df_train, df_val, df_test, y_train, y_val, y_test

@task(name="dict_vectorizer")
def dict_vectorizer(df_train, df_val, df_test):
    #<h3> Dict Vectorizer </h3>
    numerical = ['registration_init_time', 'num_25', 'num_50', 'num_75', 'num_985', 'num_100', 'num_unq', 'total_secs']
    categorical = ['gender', 'registered_via', 'city']

    train_dicts = df_train[categorical + numerical].to_dict(orient='records')
    val_dicts = df_val[categorical + numerical].to_dict(orient='records')
    test_dicts = df_test[categorical + numerical].to_dict(orient='records')
    dv = DictVectorizer(sparse=False)
    X_train = dv.fit_transform(train_dicts)
    X_val = dv.fit_transform(val_dicts)
    X_test = dv.fit_transform(test_dicts)

    with open('models/preproccesor.bin', 'wb') as f_out:
        pickle.dump((dv), f_out)


    return X_train, X_val, X_test, dv

@task(name="train_model_predict", log_prints=True)
def train_model_predict(model, X_train, y_train, X_val, y_val, X_test, y_test):

    #Fit model
    model.fit(X_train, y_train)

    #predict X_val
    y_pred = model.predict(X_val)
    
    val_accuracy = accuracy_score(y_val, y_pred)
    val_precision = precision_score(y_val, y_pred)
    val_recall = recall_score(y_val, y_pred)
    val_f1 = f1_score(y_val, y_pred)
    val_score = roc_auc_score(y_val, y_pred)
    # score

    #predict X_test
    y_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    test_precision = precision_score(y_test, y_pred)
    test_recall = recall_score(y_test, y_pred)
    test_f1 = f1_score(y_test, y_pred)
    test_score = roc_auc_score(y_val, y_pred)

    log_metrics = dict()

    log_metrics = {
        'val_accuracy': val_accuracy,
        'val_precision': val_precision,
        'val_recall': val_recall,
        'val_f1': val_f1,
        'val_score': val_score,

        'test_accuracy': test_accuracy,
        'test_precision': test_precision,
        'test_recall': test_recall,
        'test_f1': test_f1,
        'test_score': test_score,
    }

    print("Validation model Score...")
    print('Algorithm:', type(model).__name__)
    print('Accuracy Score', '{:.4f}'.format(val_accuracy))
    print('Precision Score', '{:.4f}'.format(val_precision))
    print('Recal score', '{:.4f}'.format(val_recall))
    print('F1 score', '{:.4f}'.format(val_f1))
    print('ROC AUC score', '{:.4f}'.format(val_score))
    print("Evaluated validation model successfully...")
    
    print("Test model Score...")
    print('Algorithm:', type(model).__name__)
    print('Accuracy Score', '{:.4f}'.format(test_accuracy))
    print('Precision Score', '{:.4f}'.format(test_precision))
    print('Recal score', '{:.4f}'.format(test_recall))
    print('F1 score', '{:.4f}'.format(test_f1))
    print('ROC AUC score', '{:.4f}'.format(val_score))
    print("Evaluated test model successfully...")

    return log_metrics

@flow(name="run_model", log_prints=True, task_runner=SequentialTaskRunner())
def run_model(X_train, y_train, X_val, y_val, X_test, y_test):

    # mlflow.sklearn.autolog()

    # run = mlflow.active_run()
    # if(run.info.status == 'RUNNING'):
    #    mlflow.end_run()

    models = [LogisticRegression(), 
            #   RandomForestClassifier(), 
            #   KNeighborsClassifier(), 
              DecisionTreeClassifier(), 
            #   LGBMClassifier()
            ]

    models_dict = {
        0: "LogisticRegression", 
        # 1: "RandomForestClassifier", 
        # 1: "KNeighborsClassifier", 
        1: "DecisionTreeClassifier", 
        # 3: "LGBMClassifier"
    }

    for i, model in enumerate(models):

        print("Currently running: ",models_dict[i])

        with mlflow.start_run():
            mlflow.set_tag("developer", "st")
            mlflow.set_tag("model", models_dict[i])

            metrics = train_model_predict(model, X_train, y_train, X_val, y_val, X_test, y_test)
            mlflow.log_metrics(metrics)


            with open(f'models/{models_dict[i]}.bin', 'wb') as f_out:
                pickle.dump(model, f_out)

            mlflow.log_artifact(local_path=f"models/{models_dict[i]}.bin", artifact_path="artifact_pickle")
            
            if(models_dict[i]=="LGBMClassifier"):
                mlflow.lightgbm.log_model(model,artifact_path="models_pickle")
            else:
                mlflow.sklearn.log_model(model,artifact_path="models_pickle")

            mlflow.end_run()



@flow(name="main", log_prints=True)
def main(filepath='./kkbox-churn-prediction-challenge'):

    print("hello")

    #Set mlflow tracking uri and experiment
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("kkbox-churn-prediction3")

    # #Load dataset
    # df_train_dataset, df_members_v3, df_user_logs_v2 = read_data(filepath)

    # #Preprocessing data
    # df_train_dataset, df_members_v3, df_user_logs_v2 = pre_merge_processing(df_train_dataset, df_members_v3, df_user_logs_v2)

    # #Merge datasets
    # df_train = merge(df_train_dataset, df_members_v3)
    # df_train = merge(df_train, df_user_logs_v2)

    # #Post merge processing
    # df_train = post_merge_processing(df_train)

    # #Train, validation, test split
    # df_full, df_train, df_val, df_test, y_train, y_val, y_test = split_data(df_train)

    # #Save train, validation, test to pickle
    # save_pickle_dataset(df_full, df_train, df_val, df_test, y_train, y_val, y_test)

    #Read train, validation, test from pickle
    df_full, df_train, df_val, df_test, y_train, y_val, y_test = read_pickle_dataset()

    #Fit_transform train dataframe
    X_train, X_val, X_test, dv = dict_vectorizer(df_train, df_val, df_test)

    #Modeling:
    run_model(X_train, y_train, X_val, y_val, X_test, y_test)


def deploy():
    deployment = Deployment.build_from_flow(
    name="subscriber_churn_prediction",
    flow=main,
    schedule=CronSchedule(cron="10 0 5 * *"), # At 10:00 AM on the fifth day of every month 
    tags=["Kkbox Churn Prediction"]
    )
    deployment.apply()

if __name__ == '__main__':
    # deploy()
    main()