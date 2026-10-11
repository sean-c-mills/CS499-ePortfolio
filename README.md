# CS499-ePortfolio
Computer Science capstone ePortfolio for CS 499 at Southern New Hampshire University.

# Animal Shelter Dashboard

This project is an enhanced version of the Animal Shelter Dashboard originally created for CS 340 Client/Server Development and improved for the CS 499 Computer Science Capstone.

The dashboard uses Python, Dash, and MongoDB. It allows users to browse animal records, search for rescue candidates, and manage rescue profiles.

## Features

- Browse animal records
- Search for rescue candidates
- Rank eligible animals
- View breed charts
- View animal locations on a map
- Create, edit, and delete rescue profiles
- Store rescue profiles in MongoDB
- Validate animal and rescue-profile data
- Use a MongoDB index to improve rescue searches
- Store database credentials outside of the source code

## Requirements

The following software will be needed:

- Python 3
- MongoDB Server
- Jupyter Notebook or JupyterLab

MongoDB Compass is optional and is not required to run the dashboard.

Install the Python packages with:

```
pip install -r requirements.txt
```

## MongoDB Setup

MongoDB Server must be running before the dashboard is started.

The MongoDB username and password are stored in environment variables.

On Windows, they can be set with:

```
setx AAC_MONGO_USERNAME "your_username"
setx AAC_MONGO_PASSWORD "your_password"
```

The default database settings are:

```
Host: localhost
Port: 27017
Database: aac
```

The MongoDB user must have read and write access to the `aac` database.

## Set Up the Database

From the main project folder, run:

```
python -m scripts.Setup_Database
```

The setup script:

- Loads the animal data if the database is empty
- Loads the default rescue profiles
- Applies database validation
- Creates the rescue-search index

The setup script can be run again without creating duplicate animal records.

## Run the Dashboard

Open:

```
ProjectTwoDashboard.ipynb
```

Run the dashboard cell in Jupyter Notebook or JupyterLab.

The dashboard will run at:

```
http://127.0.0.1:8051/
```

## Database Testing

The database index benchmark can be run with:

```
python -m tests.Database_Index_Benchmark
```

The results are saved to:

```
tests/Database_Index_Benchmark_Results.csv
```

The benchmark compares rescue-search performance before and after the MongoDB index is added.

## Notes

MongoDB Compass is not required. The dashboard connects directly to MongoDB Server through PyMongo.

Database usernames and passwords should not be stored directly in the source code.
