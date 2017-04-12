from django.contrib import admin

# Register your models here.
from .models import Test
admin.site.register(Test)

from .models import TestSuite
admin.site.register(TestSuite)

from .models import TestStep
admin.site.register(TestStep)

