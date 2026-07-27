from django.contrib import admin
from .models import Agent, Budget, FinancialMetric, QueryLog, Report, Task,FinancialUpload

admin.site.register(Agent)
admin.site.register(FinancialMetric)
admin.site.register(QueryLog)
admin.site.register(Budget)
admin.site.register(Task)
admin.site.register(Report)
admin.site.register(FinancialUpload)