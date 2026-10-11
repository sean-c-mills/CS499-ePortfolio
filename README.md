# CS499-ePortfolio

Computer Science capstone ePortfolio for CS 499 at Southern New Hampshire University.

The repository contains the original Animal Shelter Dashboard and the three enhanced versions created during CS 499:

- Software Design and Engineering
- Algorithms and Data Structures
- Databases

The Database enhancement is the final version of the application and includes the work completed during the earlier enhancements.

[View the CS 499 ePortfolio](https://sean-c-mills.github.io/CS499-ePortfolio/)

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

A copy of `requirements.txt` is included at the repository root and inside the final Database enhancement folder.

From the repository root, install the Python packages with:

```bash
pip install -r requirements.txt
```

## Final Application Location

The completed version of the Animal Shelter Dashboard is located in:

```text
artifacts/CS340 Artifact Enhancement 3 - Databases
```

Before running the database setup, dashboard, or benchmark, open a terminal in that folder.

On Windows, from the repository root, this can be done with:

```bash
cd "artifacts/CS340 Artifact Enhancement 3 - Databases"
```

## MongoDB Setup

MongoDB Server must be running before the dashboard is started.

The MongoDB username and password are stored in environment variables.

On Windows, they can be set with:

```bash
setx AAC_MONGO_USERNAME "your_username"
setx AAC_MONGO_PASSWORD "your_password"
```

The default database settings are:

```text
Host: localhost
Port: 27017
Database: aac
```

The MongoDB user must have read and write access to the `aac` database.

## Set Up the Database

From the `CS340 Artifact Enhancement 3 - Databases` folder, run:

```bash
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

```text
ProjectTwoDashboard.ipynb
```

Run the dashboard cell in Jupyter Notebook or JupyterLab.

The dashboard will run at:

```text
http://127.0.0.1:8051/
```

## Database Testing

The database index benchmark can be run from the `CS340 Artifact Enhancement 3 - Databases` folder with:

```bash
python -m tests.Database_Index_Benchmark
```

The results are saved to:

```text
tests/Database_Index_Benchmark_Results.csv
```

The benchmark compares rescue-search performance before and after the MongoDB index is added.

## Notes

MongoDB Compass is not required. The dashboard connects directly to MongoDB Server through PyMongo.

Database usernames and passwords should not be stored directly in the source code.
