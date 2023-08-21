# Course MLOps-Zoomcamp Capstone Project

## Project name

**KKbox streaming churn prediction**

<img src="">

## Project evaluation rubrics:
https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/07-project

## Project description

Capstone project for the course `mlops-zoomcamp` from [DataTalksClub](https://github.com/DataTalksClub/mlops-zoomcamp).

**Project pain point**:

KKBOX is Asia’s leading music streaming service, holding the world’s most comprehensive Asia-Pop music library with over 30 million tracks. They offer a generous, unlimited version of their service to millions of people, supported by advertising and paid subscriptions. This delicate model is dependent on accurately predicting churn of their paid users.

The aim of this project is provide an API service to predict subscribers who might **Churn** in the following month.

The solution for this churn problem is implemented using **MLflow with AWS EC2 and S3**, pipeline automation using **Prefect Cloud**, and observability using **Evidently**, **Prometheus**, and **Grafana**.

## Dataset

The dataset for this project is part of the Kaggle competition - [Kkbox churn prediction] (https://www.kaggle.com/c/kkbox-churn-prediction-challenge)

Data dictionary: [Dataset](./kkbox-churn-prediction-challenge/dataset_README.md)

Download the datasets provided in the Kaggle competition.

## Project Configuration

This project is implemented on `Amazon Linux` on AWS as below:

Platform details: Linux

AMI name:  amzn2-ami-kernel-5.10-hvm-2.0.20230628.0-x86_64-gp2

Reproducibility are based on specific configuration above; Locally on Macbook M1 Pro

## Project structure

This project repository contains the main folder, a README.md, and a subfolder for the dataset ()

a. dataset folder contains train and test datasets.
b. code/main folder contains the main source code with configurations file includes.

  - Dockerfile
  - docker-compose.yml
  - MLflow database
  - Prefect database
  - Prediction service
  - CI/CD pipeline (to be verified)
  - Integration test (to be verified)


## Project overview/instructions:

The project starts with exploring the train, members, and user_logs datasets "`data_explore.ipynb`" and merging them "`EDA_merge.ipynb`" to create the final train dataset. 

The data exploration and merge phases consisted of cleaning the dataset pre and post merge to discard any anamolies and make up for missing data. The resulting train, test, validation datasets are stored on the local system using pickle.

Once the dataset was ready the project splits the dataset into train, test, and validation and worked on the modeling "`model training.ipynb`". The project implementation experiments with different models. The model experimentation was done with the help of mlflow server and database as seen in the jupyter notebook "`model training mlflow.ipynb`". Once the desired accuracy is found the model is promoted to the model registry with "`model mlflow registry.ipynb`", storing the model artifacts and saving the model as a pickle file.
**MLflow** was used for model experiment tracking, model registry, and to store the model artifacts using "`mlflow.db`" 

Furthermore, AWS EC2 in the cloud is ued to host the **MLflow** tracking server and used an S3 bucket to store the artifacts in "`model mlflow aws cloud.ipynb`"

The pipeline of this model was built using **Prefect**. Prefect helps with the workflow orchestration for this project by running the pipelines based on the assigned `task` and `flow` tags. I have also included the deployment schedule. All the deployments and runs are tracked on **Prefect Cloud**

The project has deployed the model in Prefect to run at 10:00 AM on the fifth day of every month 

Ideally, a churn prediction model like this would be deployed as a batch pipeline which would provide data for high risk subscribers whom can be targeted with retention incentives. However, as an addition, the project here also provides the business/customer care user with the ability to predict churn risk for a subscriber by providing user metadata, and user log details. This ad-hoc ability is provided using **Flask**.


As for data quality and monitoring, the project implements **Evidently**, **Prometheus**, and **Grafana** to data monitoring team by analyzing the real-time peformance metrics.
  
## Project instructions

### Step 1. Clone github repository

```bash
git clone https://github.com/sarthz/mlops-zoomcamp.git
```

Clone the project to the local server.

### Step 2. Navigate to the project directory

```bash
cd ./capstone_project
```

### Step 3. Build the services using docker compose

```bash
docker-compose up --build
```

This command will run the docker-compose to build up the services and dependencies for the services.

**NOTE**: Add `-d` to run in the detach mode


### Step 4. MLflow preparation (cloud version)

```bash
mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://mlflow:XeUxRgJfLRbdPD0zveoD@mlflow-database.cwcwp86pkdi8.us-east-2.rds.amazonaws.com:5432/mlflow_db --default-artifact-root s3://mlflow-artifacts-remote-st
```

### Step 5. Prefect Flow

You can run the "`model prefect_flow.py`" script to run the deployment in **Prefect Cloud**

```bash
prefect config set PREFECT_API_URL="http://0.0.0.0:4200/api" # local server
prefect orion start --host 0.0.0.0
```

The command above will set the `PREFECT API URL` at localhost with port 4200 and start `prefect orion` 

**link**: http://0.0.0.0:4200/

**NOTE**: for use prefect as remote server need to set with the command:

```bash
prefect config set PREFECT_ORION_UI_API_URL="http://<external ip>:4200/api" # Remote server
```

### Step 6. MLflow Model training and monitoring

```bash
python model training.ipynb
```

Run python script `model_training.py` to start training the model. To save time you could only use the `DecisionTreeClassifier` to predict churn.

You could track the results on `MLflow UI` or `Prefect UI`.

There are provision in the "`model mlflow registry`" to promote the model to the `Staging` and `Product` via `MLflow Client`.


### Step 7. Model prediction

To test the model using the api you could use the "`predict.py`" and "`test.py`" to 

```bash
python test.py
```

### 8. Model & Data monitoring

The **Grafana dashboard** is used to monitor and check performance metrics.


## Future Scope

1. Automate extract, cleaning, loading of the next month's dataset and predicting churn for the following month

2. Initiate the CI/CD pipeline to help deploy the solution in a automated way

3. Model tuning

## Tech Stack

- MLflow
- AWS EC2
- S3 Bucket
- Prefect Cloud
- Flask
- Grafana
- Prometheus
- Evidently
- Postgres
- Docker
