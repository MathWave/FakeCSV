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
        sep = dataset.schema.separator.separator
        char = dataset.schema.string_character.character
        columns = [col.name for col in dataset.schema.columns]
        total = {
            col: [] for col in columns
        }
        for _ in range(rows):
            for col in dataset.schema.columns:
                validator = eval(col.col_type.validator)()
                args = []
                ex = loads(col.extras)
                for key in ex.keys():
                    lo = loads(col.col_type.specials)[key]
                    ar = f'({ex[key]})'
                    fun = eval(lo + ar)
                    args.append(fun)
                data = validator.create(*args)
                total[col.name].append(data)
        df = pd.DataFrame(total)
        df.to_csv(dataset.file.path, sep=sep, quotechar=char)
        dataset.status = 'R'
        dataset.save()
    except Exception as e:
        dataset.status = 'F'
        dataset.save()
        print(e)


def download_file(dataset_id):
    ds = DataSet.objects.get(id=dataset_id)
    filename = ds.file.path

