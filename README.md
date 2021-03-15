# Teachers Volunteering Project

## Introduction
Volunteering is a platform that enables users i.e unemployed teachers, undergraduates pursuing teaching as a profession and anyone with teaching personnel, to view how resources(teachers) are distributed in Tanzania and identify where help is needed most thus applying.

## Languages Used
- Python 
> Django Framework

- SQL
> SQLite as a backend in Development

> PostgreSQL in Production

## Minimum Skills Required
Intermediate+ in Programming:
> Object Oriented Programming

Intermediate+ Django Coding Skills:
> Django 3.+

Beginner+ in JavaScript:
> ECS6+ Syntax

Beginner+ in HTML:
> With CSS & Bootstrap in designing

## Quick Start
Installation steps in your terminal (MacOS or Linux) or CMD (Windows)

  ```git

   git clone https://gitlab.com/hamisap/vp.git
   
   ```
   ```cmd
   cd tvs-master
   ```
   ```python
   virtualenv -p python3.76 # Your Python version
   source venv/bin/activate
   pip install spacy
   pip install nltk
   python -m spacy download en_core_web_sm
   python -m nltk.downloader words
   python -m nltk.downloader stopwords
   pip install -r dependencies.txt
   pip list -o --format columns|  cut -d' ' -f1|xargs -n1 pip install -U
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic
   python manage.py runserver # Start the application server
   ```

Provided Django & It's environment is installed in the system type in your terminal (MacOS or Linux) or CMD (Windows).

   ```git
   git clone https://gitlab.com/hamisap/vp.git
   ```
   ```c#
   cd tvs-master
   ```
   ```python
   workon (your-environment)
   pip install spacy
   pip install nltk
   python -m spacy download en_core_web_sm
   python -m nltk.downloader words
   python -m nltk.downloader stopwords
   pip install -r dependencies.txt
   pip list -o --format columns|  cut -d' ' -f1|xargs -n1 pip install -U
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic
   python manage.py runserver # Start the application server
   ```

## Requirements
- internet access
- python 3+
- django & it's environment installed in both server and local machine

## Recent Development Environment Details
- python 3.7.6
- current dependencies versions in dependencies.txt

## TODO List (Development)
- [x] Resume Uploading and Text Extraction
- [x] Nearby Location Detection
- [x] Charts & Graphs from models
- [x] CSV file to model (database) 
- [x] Inside Messages
- [x] Printing Functionality
- [x] Condition Interactivity (Approval/Disapproval of teachers with reasons)
- [x] Project Code Optimization & Stability  :rotating_light: 
- [x] Project Sitemaps and SSL
- [x] UIX Revamping 
- [x] Git optimization 
- [x] Session Handling
- [x] Deployment

## Remarks
- Chrome Browser is recommended in Windows and All Browsers in both Mac & Ubuntu OS.
  > Firefox and Edge for some reason does not render the high charts map and graphs unless deployed to the cloud.

- In a local machine use a worksheet not more than 1MB, less for more efficiency unless using PostgreSQL.
  > Django recommends PostgreSQL which is available in any Django supported host provider.

- Resume/CV Upload Limitation
  > PDF/DOCx Files are limited to 9MiBs, greater than this will be rejected.

- Web Push Notification Limitation
  > Unless the web app is deployed, no any web push notification will be executed.

- Migrations have been pushed to the repo for a reason, clear them for your own risks....
  > Django keeps on tracking its prevoius models for reference unless you flush the database and trigger each model.

- Unless deployed to the cloud a machine with low performance will experience some lags and delay in execution as Django does not currently supports async.
  > Django is line by line execution some of the long operations tend to be skipped (handleded some).


## Author
   **Hamisa Miraji @ 2019 - 2020**
   > UDSM Student - Bsc. In Computer Science 2017 - 2020
   > +255 714 189 035




