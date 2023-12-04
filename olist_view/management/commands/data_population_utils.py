import csv
from datetime import datetime

from django.db import models


def load_data(cls, model, csv_path, contains_fk, fk_map_pk):
    existing_count = model.objects.count()

    with open(csv_path, 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        csv_count = len(rows)

        if existing_count < csv_count:
            new_data = rows[existing_count:]
            if len(contains_fk) > 0:
                create_instances(model, new_data, contains_fk, fk_map_pk)
            else:
                model.objects.bulk_create([model(**row) for row in new_data])
            cls.stdout.write(cls.style.SUCCESS(f'{len(new_data)} rows inserted for {model.__name__}.'))
        else:
            cls.stdout.write(cls.style.SUCCESS(f'No new data to insert for {model.__name__}.'))


def create_instances(self, model, data, fk_fields, fk_map_pk):
    for row in data:
        to_insert = True
        for field in model._meta.fields:
            if isinstance(field, models.ForeignKey):
                related_model = field.related_model
                fk_value = row.pop(field.name)

                try:
                    row[field.name] = fk_fields[field.name].objects.get(
                        **{fk_map_pk[field.name]: fk_value})
                except related_model.DoesNotExist:
                    to_insert = False
                    self.stdout.write(self.style.WARNING(
                        f'Skipping row: {row}. {related_model.__name__} with {field.name}={fk_value} does not exist.'
                    ))
                    break
            elif field.get_internal_type() == "DateTimeField":
                date_string = row.pop(field.name)
                try:
                    datetime_object = datetime.strptime(date_string, '%Y-%m-%d')
                    row[field.name] = datetime_object.strftime('%Y-%m-%d')
                except ValueError:
                    try:
                        datetime_object = datetime.strptime(date_string, '%m/%d/%Y %H:%M')
                        row[field.name] = datetime_object.strftime('%Y-%m-%d')
                    except ValueError:
                        datetime_object = datetime.strptime(date_string, '%m/%d/%Y %H:%M')
                        row[field.name] = datetime_object.strftime('%Y-%m-%d')
        if to_insert:
            model.objects.create(**row)
