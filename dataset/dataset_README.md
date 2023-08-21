## Data Exploration


KKBOX offers subscription based music streaming service. When users signs up for our service, users can choose to either manual renew or auto-renew the service. Users can actively cancel their membership at any time.

The training data is selected from users whose membership expire within within the month of February 2017.

We use 3 datasets to limit the scope of this modeling as the intention of the MLOps Zoomcamp capstone project is to showcase the functionality which would support a datascience model. Hence, we focus on 3 datasets -

- the train dataset ('train.csv')
- the members metadata ('members_v3.csv')
- susbcriber logs ('user_logs_v2.csv')

Here is more information about the above 3 datasets

### Tables

### train.csv
the train set, containing the user ids and whether they have churned.

msno: user id
is_churn: This is the target variable. Churn is defined as whether the user did not continue the subscription within 30 days of expiration. is_churn = 1 means churn,is_churn = 0 means renewal.

### user_logs_v2.csv
daily user logs describing listening behaviors of a user. Data collected until 2/28/2017.

msno: user id
date: format %Y%m%d
num_25: # of songs played less than 25% of the song length
num_50: # of songs played between 25% to 50% of the song length
num_75: # of songs played between 50% to 75% of of the song length
num_985: # of songs played between 75% to 98.5% of the song length
num_100: # of songs played over 98.5% of the song length
num_unq: # of unique songs played
total_secs: total seconds played

### members.csv
user information. Note that not every user in the dataset is available.

msno
city
bd: age. Note: this column has outlier values ranging from -7000 to 2015, please use your judgement.
gender
registered_via: registration method
registration_init_time: format %Y%m%d
expiration_date: format %Y%m%d, taken as a snapshot at which the member.csv is extracted. Not representing the actual churn behavior.
members_v3.csv

