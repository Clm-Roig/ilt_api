from django.contrib import admin
from .models import Memento, MementoCategory

# Register your models here.
admin.site.register(Memento)
admin.site.register(MementoCategory)
