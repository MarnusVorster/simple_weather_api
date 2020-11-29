# Simple historical weather API

## Description
This is a basic api to fetch weather for a specific city/town using django as rest framework and RapidAPI to fetch the historical data.

## Setup and how to run

### Python
This was created on python 3.8, but should work fine on 3.6 and 3.7.

### pip
Pip install the requirements as follows:  
`pip install -r requirements.txt`

### env vars (For development)
Then copy `.env.template` as `.env` and populate the variables.
alternatively set the vars as follows:  
```
export WEATHER_API_KEY=<some_value>
export PUBLIC_IP=<some_value>
```
The `PUBLIC_IP` is used in django to allow external connections.

### Running
To run the API server execute the following:  
`python manage.py runserver <private_ip>:<port_to_listen_on>`

### Deploy
The `deploy_script.sh` was designed to be deployed and run on a AWS EC2 instance.  
It can be modified to suite your needs.

## Testing
To run tests execute the following (Make sure the env vars exists):  
`python manage.py test`

## API Usage
To use the API, start the django service and in a rest API client of your choice:  
Do a *GET* to `http://<your_ip>:<chosen_port>/weather_lookup/search` with payload  
```json
{
    "city": "City To Search For",
    "period": 1 // The period in days to do a historical lookup on.
}
```
The response should look something like:  
```json
{
  "min": 15.5,
  "max": 30.0,
  "avg": 22.5,
  "median": 21.5
}
```

## TODO's
- Add functionality to support multiple weather API's
- Add config to be deployable on AWS Lambda
