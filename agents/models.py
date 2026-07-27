from django.db import models

class Agent(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class FinancialMetric(models.Model):

    month = models.CharField(
        max_length=50,
        unique=True
    )

    revenue = models.DecimalField(max_digits=15, decimal_places=2)

    expenses = models.DecimalField(max_digits=15, decimal_places=2)

    ebitda = models.DecimalField(max_digits=15, decimal_places=2)

    cash_position = models.DecimalField(max_digits=15, decimal_places=2)

    budget = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.month
    
class QueryLog(models.Model):
    question = models.TextField()
    agent_name = models.CharField(max_length=100)
    response = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.agent_name} - {self.created_at}"
    
class Budget(models.Model):
    department = models.CharField(max_length=100)

    budget_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    actual_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.department

class Task(models.Model):

    title = models.CharField(max_length=255)

    description = models.TextField()

    status = models.CharField(
        max_length=50,
        default="Pending"
    )

    priority = models.CharField(
        max_length=50,
        default="Medium"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
    
class Report(models.Model):

    report_type = models.CharField(
        max_length=100
    )

    summary = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.report_type
    
class FinancialUpload(models.Model):
    file_name = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to="financial_uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name