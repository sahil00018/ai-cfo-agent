from agents.models import FinancialMetric
from .treasury_agent import analyze_cash
from .budget_agent import analyze_budget
from agents.services.ai_service import ask_gemini


def analyze_financial_health(question):

    records = FinancialMetric.objects.order_by("-created_at")[:2]

    if len(records) < 2:
        return {
            "agent": "Financial Health Agent",
            "health_score": 0,
            "status": "No Data",
            "strengths": [],
            "weaknesses": [],
            "recommendations": ["Please upload at least two financial records."],
            "ai_insight": "Not enough financial data available."
        }

    current = records[0]
    previous = records[1]

    treasury = analyze_cash(question)
    budget = analyze_budget(question)

    score = 100

    # Revenue
    if current.revenue < previous.revenue:
        score -= 15

    # EBITDA
    if current.ebitda < previous.ebitda:
        score -= 20

    # Liquidity
    if treasury["liquidity_status"] != "Healthy":
        score -= 15

    # Budget
    if budget["status"] == "Overspending":
        score -= 20

    if score >= 80:
        status = "Healthy"
    elif score >= 60:
        status = "Moderate Risk"
    else:
        status = "High Risk"

    strengths = []
    weaknesses = []
    recommendations = []

    if current.cash_position > 30000:
        strengths.append("Cash position remains stable.")

    if current.revenue < previous.revenue:
        weaknesses.append("Revenue decline detected.")
        recommendations.append("Focus on revenue growth initiatives.")

    if current.ebitda < previous.ebitda:
        weaknesses.append("EBITDA has decreased significantly.")
        recommendations.append("Reduce operating expenses and improve profitability.")

    if budget["status"] == "Overspending":
        weaknesses.append("Budget overspending observed.")
        recommendations.append("Strengthen budget controls.")

    if treasury["liquidity_status"] != "Healthy":
        recommendations.append("Monitor cash flow and working capital closely.")

    prompt = f"""
You are an expert CFO.

Financial Health Score: {score}

Status: {status}

Strengths:
{strengths}

Weaknesses:
{weaknesses}

Recommendations:
{recommendations}

Provide a short executive management insight.
"""

    try:
        ai_insight = ask_gemini(prompt)
    except Exception:
        ai_insight = "AI insight generation is temporarily unavailable."

    return {
        "agent": "Financial Health Agent",
        "health_score": score,
        "status": status,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "ai_insight": ai_insight
    }