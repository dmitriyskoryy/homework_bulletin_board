from django.contrib import admin

from .models import *


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Adt)
admin.site.register(Respond)
admin.site.register(Subscriber)

