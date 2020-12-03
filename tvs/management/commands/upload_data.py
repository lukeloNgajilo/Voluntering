from csv import DictReader

from django.core.management import BaseCommand

from tvs import models

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from a csv file into the database (almost 50 min)"

    def handle(self, *args, **options):

        if models.Chart.objects.exists():
            print('data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return

        print("Loading data available")
        for row in DictReader(open('media/documents/test2.csv')):
            data = models.Chart()
            data.region = row['REGION']
            # data.council = row['COUNCIL']
            # data.ward = row['WARD']
            # data.school = row['SCHOOL NAME']
            data.enrolment = row['ENROLMENT']
            data.teacher = row['ALL TEACHERS']
            data.ptr = row['PTR']
            data.save()
