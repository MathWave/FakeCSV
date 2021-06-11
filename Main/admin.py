from django.contrib import admin
from Main.models import Schema, Column, ColumnType, Separator, StringCharacter, DataSet

admin.site.register(Schema)
admin.site.register(Column)
admin.site.register(ColumnType)
admin.site.register(Separator)
admin.site.register(StringCharacter)
admin.site.register(DataSet)
