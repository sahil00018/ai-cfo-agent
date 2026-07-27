from .fpna_agent import analyze_finance
from .treasury_agent import analyze_cash
from .budget_agent import analyze_budget
from .reporting_agent import generate_report
from .audit_agent import audit_analysis
from .compliance_agent import compliance_analysis
from .risk_agent import risk_analysis
from .financial_health_agent import analyze_financial_health
from agents.services.ai_service import classify_question


def route_query(question):

    if not question:
        return {
            "agent": "Chief CFO Agent",
            "analysis": "No question provided.",
            "recommendation": "Please enter a valid question."
        }

    # -------------------------
    # Try Gemini Routing
    # -------------------------
    try:
        selected_agent = classify_question(question)

        print(f"Gemini Selected: {selected_agent}")

    except Exception as e:

        print(f"Gemini Error: {e}")
        print("Using Fallback Keyword Router")

        question_lower = question.lower()

        if any(keyword in question_lower for keyword in [
            "ebitda",
            "revenue",
            "profit",
            "margin",
            "forecast",
            "growth"
        ]):
            selected_agent = "FP&A Agent"

        elif any(keyword in question_lower for keyword in [
            "cash",
            "liquidity",
            "working capital",
            "bank balance"
        ]):
            selected_agent = "Treasury Agent"

        elif any(keyword in question_lower for keyword in [
            "budget",
            "variance",
            "actual spending",
            "overspend",
            "overspending"
        ]):
            selected_agent = "Budget Agent"

        elif any(keyword in question_lower for keyword in [
            "report",
            "mis",
            "dashboard",
            "board report",
            "investor report",
            "executive report"
        ]):
            selected_agent = "Reporting Agent"

        elif any(keyword in question_lower for keyword in [
            "audit",
            "fraud",
            "transaction validation",
            "internal audit"
        ]):
            selected_agent = "Audit Agent"

        elif any(keyword in question_lower for keyword in [
            "gst",
            "tax",
            "compliance",
            "regulatory",
            "filing"
        ]):
            selected_agent = "Compliance Agent"

        elif any(keyword in question_lower for keyword in [
            "risk",
            "vendor risk",
            "credit risk",
            "financial risk"
        ]):
            selected_agent = "Risk Agent"
        elif any(keyword in question_lower for keyword in [
            "financial health",
            "health score",
            "company health",
            "financial status"
        ]):
            selected_agent = "Financial Health Agent"

        else:
            selected_agent = "FP&A Agent"

    # -------------------------
    # Execute Selected Agent
    # -------------------------

    if selected_agent == "FP&A Agent":
        return analyze_finance(question)

    elif selected_agent == "Treasury Agent":
        return analyze_cash(question)

    elif selected_agent == "Budget Agent":
        return analyze_budget(question)

    elif selected_agent == "Reporting Agent":
        return generate_report(question)

    elif selected_agent == "Audit Agent":
        return audit_analysis(question)

    elif selected_agent == "Compliance Agent":
        return compliance_analysis(question)

    elif selected_agent == "Risk Agent":
        return risk_analysis(question)

    elif selected_agent == "Financial Health Agent":
        return analyze_financial_health(question)

    return {
        "agent": "Chief CFO Agent",
        "analysis": "Unable to determine the correct agent.",
        "recommendation": "Please rephrase your question."
    }