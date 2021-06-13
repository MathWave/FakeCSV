from json import loads, dumps
from FakeCSV.celery import app
from Main.models import DataSet
import pandas as pd
from Main.validators import *


@app.task
def generate_csv(dataset_id, rows):
    dataset = DataSet.objects.get(id=dataset_id)
    dataset.status = 'P'
    dataset.save()
    try:
        total = {}
        for col in dataset.schema.columns:
            validator = eval(col.col_type.validator)()
            args = []
            for val in col.extras:
                lo = [d for d in col.col_type.specials if d['name'] == val['name']][0]['type']
                ar = f'({val["value"]})'
                fun = eval(lo + ar)
                args.append(fun)
            total[col.name] = [validator.create(*args) for _ in range(rows)]
        dataset.data = total
        dataset.status = 'R'
        dataset.save()
    except Exception as e:
        dataset.status = 'F'
        dataset.save()
        print(e)
