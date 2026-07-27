from django.urls import path
from .views import  FinancialUploadAPIView, ask_agent, financial_data_view, financial_months_view, kpi_view, query_history, task_list, task_view, update_task_status,dashboard_view,history_view,report_view

urlpatterns = [
    path("ask/", ask_agent),
    path('query-history/', query_history),
    path('task/', task_list),
    path('tasks/update/', update_task_status),
    path('dashboard/', dashboard_view),
    path('history/', history_view),
    path('reports/', report_view),
    path('tasks/', task_view),
    path('kpis/', kpi_view),
    path("financial-data/", financial_data_view),
    path("financial-data/months/", financial_months_view),
    path("upload/", FinancialUploadAPIView.as_view(), name="upload-financial-data")
]