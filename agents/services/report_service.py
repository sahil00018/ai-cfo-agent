from agents.models import Report


def get_reports():

    reports = Report.objects.all().order_by("-created_at")

    data = []

    for report in reports:
        data.append({
            "id": report.id,
            "report_type": report.report_type,
            "summary": report.summary,
            "created_at": report.created_at
        })

    return data