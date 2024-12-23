from django.contrib import admin
from .models import operation_status_Info,cells_Info,parts_Info,machines_Info

# Register your models here.
admin.site.register(machines_Info)
admin.site.register(parts_Info)
admin.site.register(cells_Info)
admin.site.register(operation_status_Info)
