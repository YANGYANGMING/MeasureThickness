from django.contrib import admin
from thickness import models

admin.site.register(models.DataFile)
admin.site.register(models.DataSetCondition)
admin.site.register(models.DataTag)
admin.site.register(models.VersionToThcikness)
admin.site.register(models.Version)