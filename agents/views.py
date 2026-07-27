from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services.chief_agent import handle_query
from .models import FinancialMetric, QueryLog, Task
from .serializers import AskAgentSerializer, FinancialMetricSerializer, QueryLogSerializer, TaskSerializer
from rest_framework import status
from .services.dashboard_service import get_dashboard_data
from .services.history_service import get_query_history
from .services.report_service import get_reports
from .services.task_service import get_tasks
from .services.kpi_service import get_kpis
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .permissions import (
    IsCFOOrAdmin,
    IsFinanceManagerOrAdmin,
    IsAuditorOrAdmin,
)
from .pagination import CustomPagination
from django.db.models import Q
import pandas as pd
from .models import FinancialUpload
from .serializers import FinancialUploadSerializer
from rest_framework.views import APIView
from django.db import transaction

@api_view(['POST'])
def ask_agent(request):

    serializer = AskAgentSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    question = serializer.validated_data["question"]

    result = handle_query(question)

    QueryLog.objects.create(
        question=question,
        agent_name=result.get("agent"),
        response=str(result)
    )

    return Response(result)

@api_view(['GET'])
def query_history(request):

    logs = QueryLog.objects.order_by('-created_at')

    serializer = QueryLogSerializer(logs, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def task_list(request):

    tasks = Task.objects.order_by('-created_at')

    serializer = TaskSerializer(tasks, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def update_task_status(request):

    task_id = request.data.get("task_id")
    new_status = request.data.get("status")

    try:
        task = Task.objects.get(id=task_id)

        task.status = new_status
        task.save()

        return Response({
            "message": "Task updated successfully",
            "task_id": task.id,
            "new_status": task.status
        })

    except Task.DoesNotExist:
        return Response(
            {"error": "Task not found"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(["GET"])
@permission_classes([IsCFOOrAdmin])
def dashboard_view(request):    

    data = get_dashboard_data()

    return Response(data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def history_view(request):

    data = get_query_history()

    return Response(data)

@api_view(["GET"])
@permission_classes([IsAuditorOrAdmin])
def report_view(request):  

    data = get_reports()

    return Response(data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from .pagination import CustomPagination


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_view(request):

    # Read query parameters
    status = request.query_params.get("status")
    priority = request.query_params.get("priority")
    search = request.query_params.get("search")

    # Get all tasks
    tasks = Task.objects.order_by("-created_at")

    # Filter by status
    if status:
        tasks = tasks.filter(status=status)

    # Filter by priority
    if priority:
        tasks = tasks.filter(priority=priority)
    
    if search:
        tasks = tasks.filter(
        Q(title__icontains=search) |
        Q(description__icontains=search)
    )

    # Pagination
    paginator = CustomPagination()
    paginated_tasks = paginator.paginate_queryset(tasks, request)

    serializer = TaskSerializer(paginated_tasks, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(["GET"])
@permission_classes([IsFinanceManagerOrAdmin])
def kpi_view(request):

    data = get_kpis()

    return Response(data)

@api_view(["GET"])
@permission_classes([IsFinanceManagerOrAdmin])
def financial_months_view(request):

    records = FinancialMetric.objects.order_by("-created_at")
    serializer = FinancialMetricSerializer(records, many=True)
    return Response(serializer.data)


@api_view(["GET", "PUT"])
@permission_classes([IsFinanceManagerOrAdmin])
def financial_data_view(request):

    month = request.query_params.get("month") or request.data.get("month")

    if not month:
        record = FinancialMetric.objects.order_by("-created_at").first()
    else:
        record = FinancialMetric.objects.filter(month=month).first()

    if record is None:
        return Response(
            {"message": "No financial data found for that month."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = FinancialMetricSerializer(record)
        return Response(serializer.data)

    serializer = FinancialMetricSerializer(
        record,
        data=request.data,
        partial=True
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)

class FinancialUploadAPIView(APIView):

    permission_classes = [IsFinanceManagerOrAdmin]

    ALLOWED_EXTENSIONS = (".csv", ".xlsx", ".xls")
    MAX_FILE_SIZE_MB = 5
    REQUIRED_COLUMNS = {"Month", "Revenue", "Expenses", "EBITDA", "Cash", "Budget"}

    def post(self, request):

        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "No file uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_name_lower = file.name.lower()

        if not file_name_lower.endswith(self.ALLOWED_EXTENSIONS):
            return Response(
                {"error": "Unsupported file type. Please upload a .csv, .xlsx, or .xls file."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if file.size > self.MAX_FILE_SIZE_MB * 1024 * 1024:
            return Response(
                {"error": f"File is too large. Maximum size is {self.MAX_FILE_SIZE_MB}MB."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if file_name_lower.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
        except Exception as e:
            print(f"File parse error: {e}")
            return Response(
                {"error": "Unable to read this file. Make sure it's a valid CSV or Excel file."},
                status=status.HTTP_400_BAD_REQUEST
            )

        df.columns = df.columns.astype(str).str.strip()

        missing_columns = self.REQUIRED_COLUMNS - set(df.columns)
        if missing_columns:
            return Response(
                {"error": f"Missing required columns: {', '.join(sorted(missing_columns))}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if df.empty:
            return Response(
                {"error": "The uploaded file has no data rows."},
                status=status.HTTP_400_BAD_REQUEST
            )

        numeric_columns = ["Revenue", "Expenses", "EBITDA", "Cash", "Budget"]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        if df[numeric_columns].isnull().any().any():
            bad_rows = df[df[numeric_columns].isnull().any(axis=1)]
            bad_months = bad_rows["Month"].astype(str).tolist()
            return Response(
                {"error": f"Some rows have missing or non-numeric values in: {', '.join(bad_months)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        upload = FinancialUpload.objects.create(
            file_name=file.name,
            uploaded_file=file
        )

        rows_created = 0
        rows_updated = 0

        try:
            with transaction.atomic():
                for _, row in df.iterrows():
                    month_value = str(row["Month"]).strip()

                    obj, created = FinancialMetric.objects.update_or_create(
                        month=month_value,
                        defaults={
                            "revenue": float(row["Revenue"]),
                            "expenses": float(row["Expenses"]),
                            "ebitda": float(row["EBITDA"]),
                            "cash_position": float(row["Cash"]),
                            "budget": float(row["Budget"]),
                        },
                    )

                    if created:
                        rows_created += 1
                    else:
                        rows_updated += 1

        except Exception as e:
            print(f"Database insert error: {e}")
            return Response(
                {"error": "Something went wrong saving this data. Your previous data was kept."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = FinancialUploadSerializer(upload)

        return Response(
            {
                "message": f"File uploaded successfully — {rows_created} month(s) added, {rows_updated} month(s) updated.",
                "rows_found": len(df),
                "rows_created": rows_created,
                "rows_updated": rows_updated,
                "database_records": FinancialMetric.objects.count(),
                "columns": list(df.columns),
                "preview": df.head().to_dict(orient="records"),
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )