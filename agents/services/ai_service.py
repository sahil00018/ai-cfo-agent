import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

def classify_question(question):

    prompt = f"""
You are the routing brain of an AI CFO Platform.

Your task is to select the SINGLE BEST agent.

Available Agents:

1. FP&A Agent
Handles:
- Revenue
- EBITDA
- Profitability
- Profit
- Margins
- Forecasting
- Growth
- Financial Performance

2. Treasury Agent
Handles:
- Cash Position
- Liquidity
- Working Capital
- Bank Balance
- Cash Flow

3. Budget Agent
Handles:
- Budget
- Budget Variance
- Overspending
- Under-spending
- Actual vs Budget Analysis
- Department Spending
- Cost Control

IMPORTANT:
Any question related to budget, spending, overspending,
variance, cost control, or actual vs budget MUST go to Budget Agent.

4. Reporting Agent
Handles:
- Executive Reports
- MIS Reports
- Dashboards
- Board Reports
- Financial Summaries

5. Audit Agent
Handles:
- Audit
- Fraud Detection
- Internal Controls
- Transaction Validation

6. Compliance Agent
Handles:
- GST
- Tax
- Compliance
- Regulatory Filing

7. Risk Agent
Handles:
- Risk Management
- Vendor Risk
- Credit Risk
- Financial Risk

8. Financial Health Agent
Handles:
- Financial Health Score
- Overall Financial Status
- Company Health
- Financial Risk Assessment


Question: Why did EBITDA decrease?
Answer: FP&A Agent

Question: Revenue growth is slowing.
Answer: FP&A Agent

Question: What is our current cash position?
Answer: Treasury Agent

Question: Why are we overspending our budget?
Answer: Budget Agent

Question: Show budget variance.
Answer: Budget Agent

Question: Generate an executive financial report.
Answer: Reporting Agent

Question: Review internal audit findings.
Answer: Audit Agent

Question: Check GST compliance.
Answer: Compliance Agent

Question: Review vendor risk exposure.
Answer: Risk Agent

Question:
{question}

Return ONLY one of these exact values:

FP&A Agent
Treasury Agent
Budget Agent
Reporting Agent
Audit Agent
Compliance Agent
Risk Agent
Financial Health Agent
"""

    response = model.generate_content(prompt)

    return response.text.strip()

def analyze_financial_data(financial_data, question):

    prompt = f"""
You are an expert Chief Financial Officer (CFO).

Below is the company's uploaded financial data:

{financial_data}

User Question:
{question}

Instructions:
1. Answer ONLY using the uploaded financial data.
2. Compare months whenever appropriate.
3. Calculate trends if possible.
4. Mention financial risks.
5. Mention positive observations.
6. Give practical business recommendations.
7. If the question cannot be answered from the data, clearly say so.

Return the response in this format:

📊 Executive Summary

📈 Key Insights

⚠ Risks

✅ Recommendations
"""

    

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error: Failed to generate response from Gemini API. Details: {e}")
        return "AI analysis is temporarily unavailable."

