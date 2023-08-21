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

The solution for this churn problem is implemented using **MLflow**, pipeline automation using **Prefect**, and observability using **Evidently**, **Prometheus**, and **Grafana**.

## Dataset

The dataset for this project is part of the Kaggle competition - [Kkbox churn prediction] (https://www.kaggle.com/c/kkbox-churn-prediction-challenge)

Data dictionary: [Dataset](./kkbox-churn-prediction-challenge/dataset_README.md)


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


## Project overview

I started the project with exploring the train, members, and user_logs datasets "`data_explore.ipynb`" and merging them "`EDA_merge.ipynb`" to create the final train dataset.

The data exploration and merge phases consisted of cleaning the dataset pre and post merge to discard any anamolies and make up for missing data. The resulting train, test, validation datasets are stored on the local system using pickle.

Once the dataset was ready I split the dataset into train, test, and validation and worked on the modeling "`model training.ipynb`". I experimented with different models. The model experimentation was done with the help of mlflow server and database as seen in the jupyter notebook "`model training mlflow.ipynb`". Once I was sure of the model which gave the best results I promoted the model to the model registry with "`model mlflow registry.ipynb`", storing the model artifacts and saving the model as a pickle file.
**MLflow** was used for model experiment tracking, model registry, and to store the model artifacts using "`mlflow.db`" 

The pipeline of this model was built using **Prefect**. Prefect helps with the workflow orchestration for this project by running the pipelines based on the assigned `task` and `flow` tags. I have also included the deployment schedule 



The Prefect has been used as a workflow orchestrator in the project by deploying the project creating the `task` and `flow` and then scheduling the pipeline to run at the time the pipeline should schedule.

Now after the model training session and deployment process. The project is still not ready and needs more improvement work. This time the model should be used and serve the expected performance from the model as the application that will use by the users this application will implement using **Flask**. 

Apart from this the observability for the service is the task being implemented to ensure the operations team can observability by a combination of **Grafana**, **Prometheus**, and **Evidently** these services will provide real-time model performance and data drift from the production. So the operation can handle the problems immediately or requests other teams to help and discuss to make the decision together.

Apart from this, the observability for the service is the task being implemented to ensure the operations team can observability by a combination of **Grafana**, **Prometheus**, and **Evidently**. These services will provide real-time model performance and data drift from production. So the operation can handle the problems immediately or requests other teams to help and discuss to make the decision together.


## Demo

This demo shows the main functionality of the project and will follow by the project instructions link below.

https://www.youtube.com/watch?v=5kNUc1ebU28

<a href="https://www.youtube.com/watch?v=5kNUc1ebU28">
<img src="https://github.com/surawut-jirasaktavee/course-mlops-zoomcamp/blob/main/08-project-capstone/images/data_drift_report.png">
</a>
  
## Project instruction

### 1. Project repository

```bash
git clone https://github.com/surawut-jirasaktavee/course-mlops-zoomcamp.git
```

Clone the project to the local server.

### 2. Work directory

```bash
cd ./course-mlops-zoomcamp/08-project-capstone/code
```

Move to the `./course-mlops-zoomcamp/08-project-capstone/code` from the current directory.

### 3. Build the services up

```bash
docker-compose up --build
```

This command will run the docker-compose to build up the services and dependencies for the services.

**NOTE**: Add `-d` to run in the detach mode


### 4. Environment preparation

```bash
pipenv shell
```

This command will install all required dependencies and activtte the environment from this requisition of this project.

### 5. MLflow preparation

```bash
mlflow ui -h 0.0.0.0 -p 5050 --backend-store-uri sqlite:///customer_churn.db --default-artifact-root ./mlruns
```

This command will build the mlflow service to work in this project e.g. `database` and `MLflow UI`.

**link**: http://localhost:5050/

**MLflow tracking**
<img src="https://github.com/surawut-jirasaktavee/course-mlops-zoomcamp/blob/main/08-project-capstone/images/mlflow_tracking.png">

**MLflow registry**
<img src="https://github.com/surawut-jirasaktavee/course-mlops-zoomcamp/blob/main/08-project-capstone/images/mlflow_registry.png">

**MLflow artifactts**
<img src="https://github.com/surawut-jirasaktavee/course-mlops-zoomcamp/blob/main/08-project-capstone/images/mlflow_artifacts.png">


### 6. Prefect preparation

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

**Prefect flow**
<img src="https://github.com/surawut-jirasaktavee/course-mlops-zoomcamp/blob/main/08-project-capstone/images/prefect_flow_run.png">
<img src="https://github.com/surawut-jirasaktavee/course-mlops-zoomcamp/blob/main/08-project-capstone/images/prefect_flow.png">

**Prefect deployment**
<img src="https://github.com/surawut-jirasaktavee/course-mlops-zoomcamp/blob/main/08-project-capstone/images/prefect_deployment.png">

**Prefect workqueue**
<img src="https://github.com/surawut-jirasaktavee/course-mlops-zoomcamp/blob/main/08-project-capstone/images/prefect_workqueue.png">

**Prefect storage**
<img src="https://github.com/surawut-jirasaktavee/course-mlops-zoomcamp/blob/main/08-project-capstone/images/prefect_storage.png">

### 7. MLflow Model training and monitoring

```bash
python model_training.py
```

Run python script `model_training.py` to start training the model. For this project use `LightGBMClassifier` to classification the data between customer who will **Churn** or  **Not Churn**.

In order to inspect the training process or details apart from command line. Open the `MLflow UI` or `Prefect UI` instead.

The model will transition to the `Staging` in the `MLflow UI` after finish training session.

### 8. MLflow Model registry and artifacts

```bash
python model_registry.py
```

Run `model_registry.py` to retrieve the data of the model from the `MLflow database` and compare current model in the production with the new model. If the new model is better then transition this new model to the production and give the archive stage to the production model.

### 9. Prefect deployment

```bash
prefect deployment create model_deployment.py
```

The command above will create the deployment from `model_deployment.py` and return the **deployment ID** in the terminal.

### 10. Prefect work-queue

```bash
prefect work-queue create -d <deployment ID> <work-queue name>
```

In order to see the deployment ID run the command:

```bash
prefect deployment ls
```

The work-queue should be created.

### 11. Prefect agent

```bash
prefect agent start <work-queue ID>
```

After created the work-queue. now the `Prefect agent` can work on the deployment to help the pipeline run in the specify time by schedule the deployment

In order to see the work-queue ID run the command:

```bash
prefect work-queue ls
```

**NOTE**: For the agent start API. It has sometimes the API gets stuck with no reason for me. So if get stuck with this part just wait and skip to the next step first. Then if finish all processes and back to the agent and the agent is still stuck trying to use the UI instead. The agent should be run normally.

### 12. Model prediction

Now the model ready to use after training and deploy to the production and the services should be ready to serve the prediction result of each customer who will **Churn** or **Not Churn** from our company.

In the current directory `(./course-mlops-zoomcamp/08-project-capstone/code)` run the command below to send the data to the model service and get the results.

```bash
python customer_data.py
```

<img src="https://github.com/surawut-jirasaktavee/course-mlops-zoomcamp/blob/main/08-project-capstone/images/model_prediction.png">

this command will read the data from `./evidently_service/datasets/churn_test_dataset.csv` and send it to the `Flask` application. And the model service will send the outputs the prediction as **Churn** or **Not Churn** and write the `customer ID` and `churn result` to `./churn_report` to serve this result to the analyst team to work on this result and find the good solutions.

### 13. Model & Data monitoring

In order to inspect the `data drift` or `model drift` see the **Grafana dashboard** to monitor then check if any data show abnormal or model performance become to bad.

<img src="https://github.com/surawut-jirasaktavee/course-mlops-zoomcamp/blob/main/08-project-capstone/images/data_drift_report.png">

### 14. Service port

**All services port**
<img src="https://github.com/surawut-jirasaktavee/course-mlops-zoomcamp/blob/main/08-project-capstone/images/service_port.png">


## Future improvement

This project still need more improvement to give more abilities for work with. 

1. Add the alert when the data drift or model performance is down.

2. When the alert occurs send some triggers. For example when the model performance is down show the alert to the operation team and send the trigger to the prefect to start the model deployment to re-train the model to get better model.

3. Combine both two above with CI/CD process. This will become to CI/CD/CT pipeline and deploy to the production automatically.

4. Add others model to training session and select the best model for the project.

5. Add model optimization such as `hyperopt` to tune hyperparameters.

6. Add IaC to manage and deploy the infrastructure and services.


## Tech Stack

- Flask
- MLflow
- Prefect
- Grafana
- Prometheus
- Evidently
- Mongodb
- Docker
