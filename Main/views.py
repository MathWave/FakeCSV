from json import loads, dumps
from threading import Thread

from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.shortcuts import render

from Main.main import check_authorize
from Main.models import Schema, ColumnType, Separator, StringCharacter, Column, DataSet
from datetime import datetime

from Main.tasks import generate_csv


@check_authorize
def schemas(request):
    if request.method == 'POST':
        Schema.objects.get(id=request.POST['schema']).delete()
        return HttpResponseRedirect('/schemas')
    return render(request, 'Main/schemas.html', {
        'schemas': reversed(Schema.objects.filter(creator=request.user))
    })


@check_authorize
def new_schema(request):
    data = {
        'separator': 'Comma (,)',
        'character': 'Double-quotes (")',
        'schema_name': 'New schema',
        'columns': []
    }
    if request.method == 'GET' and 'id' in request.GET.keys():
        schema = Schema.objects.get(id=request.GET['id'])
        if schema.creator != request.user:
            return HttpResponseRedirect('/schemas')
        data['separator'] = schema.separator.description
        data['character'] = schema.string_character.description
        data['schema_name'] = schema.name
        for col in schema.columns:
            column = {
                'name': col.name,
                'type': col.col_type.name,
                'order': col.order,
                'extras': loads(col.extras)
            }
            data['columns'].append(column)
    elif request.method == 'POST':
        data = loads(request.POST['data'])
        data['separator'] = request.POST['separator']
        data['character'] = request.POST['character']
        data['schema_name'] = request.POST['schema_name']
        for key in request.POST.keys():
            if key.startswith('colname_'):
                coldata = key.split('_')
                data['columns'][int(coldata[1]) - 1]['name'] = request.POST[key]
            elif key.startswith('colorder_'):
                coldata = key.split('_')
                data['columns'][int(coldata[1]) - 1]['order'] = int(request.POST[key]) if request.POST[key].isnumeric() else data['columns'][int(coldata[1]) - 1]['order']
            elif key.startswith('colextra_'):
                coldata = key.split('_')
                data['columns'][int(coldata[1]) - 1]['extras'][coldata[2]] = request.POST[key]
        if request.POST['action'] == 'add':
            column = {
                'name': request.POST['name'],
                'type': request.POST['type'],
                'order': int(request.POST['order']) if request.POST['order'].isnumeric() else 10e10,
                'extras': {
                    val: '' for val in loads(ColumnType.objects.get(name=request.POST['type']).specials).keys()
                }
            }
            if len(data['columns']) == 0:
                column['order'] = 1
            else:
                for i in range(len(data['columns'])):
                    if data['columns'][i]['order'] >= column['order']:
                        data['columns'][i]['order'] += 1
            data['columns'].append(column)
            data['columns'].sort(key=lambda x: x['order'])
        elif request.POST['action'].startswith('delete_'):
            del data['columns'][int(request.POST['action'].split('_')[1]) - 1]
        elif request.POST['action'] == 'submit':
            for i in range(len(data['columns'])):
                data['columns'][i]['order'] = i + 1
            if 'id' in request.GET.keys():
                schema = Schema.objects.get(id=request.GET['id'])
                if schema.creator != request.user:
                    return HttpResponseRedirect('/schemas')
            else:
                schema = Schema()
            schema.name = data['schema_name']
            schema.modified_time = datetime.today()
            schema.creator = request.user
            schema.separator = Separator.objects.get(description=data['separator'])
            schema.string_character = StringCharacter.objects.get(description=data['character'])
            schema.save()
            schema.columns.delete()
            for column in data['columns']:
                Column.objects.create(
                    schema=schema,
                    col_type=ColumnType.objects.get(name=column['type']),
                    name=column['name'],
                    order=column['order'],
                    extras=dumps(column['extras'])
                )
            return HttpResponseRedirect('/schemas')
        else:
            raise AttributeError('No action')
        for i in range(len(data['columns'])):
            data['columns'][i]['order'] = i + 1
    return render(request, 'Main/new_schema.html', {
        'types': ColumnType.objects.all(),
        'separators': Separator.objects.all(),
        'string_characters': StringCharacter.objects.all(),
        'data': data
    })


@check_authorize
def fakecsv(request):
    if request.method == 'POST':
        schema = Schema.objects.get(id=request.POST['schema'])
        try:
            rows = int(request.POST['rows'])
        except ValueError:
            rows = 10
        if schema.creator != request.user:
            return HttpResponseRedirect('/')
        dataset = DataSet.objects.create(
            schema=schema,
            created=datetime.today(),
            status='I'
        )
        dataset.file.save('dataset.csv', ContentFile(''))
        flag = False
        if flag:
            generate_csv.delay(dataset.id, rows)
        else:
            Thread(target=lambda: generate_csv(dataset.id, rows)).start()
        return HttpResponseRedirect('/')
    return render(request, 'Main/fakecsv.html', {'schemas': Schema.objects.filter(creator=request.user)})


def dataset_table(request):
    if request.user.is_authenticated:
        return render(request, 'Main/dataset_table.html', {
            'datasets': DataSet.objects.filter(schema__creator=request.user).order_by('id')
        })
    return HttpResponse('')


@check_authorize
def download(request):
    obj = DataSet.objects.get(id=request.GET['id'])
    if obj.schema.creator != request.user:
        return HttpResponseRedirect('/')
    filename = obj.file.path
    response = FileResponse(open(filename, 'rb'))
    response['Content-Disposition'] = 'inline; filename=dataset.csv'
    return response
