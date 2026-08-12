"""
Ask CareerReality — RAG-style career advisor using site data + engine tool calls.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from analyzer.models import SalarySubmission, LayoffReport
from analyzer.services.salary_engine import get_salary_reality
from analyzer.services.stay_vs_switch import analyze_stay_vs_switch
from analyzer.services.offer_analyzer import OfferInput, compare_offers
from companies.models import Company
from content.models import Article
from core.models import CareerRealityIndexSnapshot


@dataclass
class AdvisorCitation:
    type: str
    label: str
    url: str


@dataclass
class AdvisorAnswer:
    answer: str
    citations: list[AdvisorCitation]
    engines_used: list[str]

    def to_dict(self) -> dict:
        return {
            "answer": self.answer,
            "citations": [{"type": c.type, "label": c.label, "url": c.url} for c in self.citations],
            "engines_used": self.engines_used,
        }


def _parse_entities(question: str) -> dict:
    """Extract salary, YOE, company mentions from natural language."""
    entities = {}
    ctc_match = re.search(r"₹?\s*(\d+(?:\.\d+)?)\s*L", question, re.I)
    if ctc_match:
        entities["ctc"] = int(float(ctc_match.group(1)))
    offer_match = re.search(r"take\s+₹?\s*(\d+(?:\.\d+)?)\s*L", question, re.I)
    if offer_match:
        entities["offer_ctc"] = int(float(offer_match.group(1)))
    yoe_match = re.search(r"(\d+)\s*YOE", question, re.I)
    if yoe_match:
        entities["yoe"] = float(yoe_match.group(1))
    for co in ["TCS", "Infosys", "Wipro", "HCL", "Accenture", "Amazon", "Google", "Microsoft", "Flipkart", "Swiggy"]:
        if co.lower() in question.lower():
            entities["company"] = co
            break
    if "startup" in question.lower():
        entities["offer_type"] = "startup"
    if any(r in question.lower() for r in ["engineer", "developer", "sde"]):
        entities["role"] = "Software Engineer"
    elif "data" in question.lower():
        entities["role"] = "Data Engineer"
    elif "product" in question.lower():
        entities["role"] = "Product Manager"
    else:
        entities.setdefault("role", "Software Engineer")
    entities.setdefault("yoe", 5)
    entities.setdefault("city", "Bengaluru")
    entities.setdefault("company_type", "service")
    return entities


def _retrieve_context(question: str, entities: dict) -> tuple[str, list[AdvisorCitation]]:
    citations = []
    context_parts = []

    # Salary data
    role = entities.get("role", "Software Engineer")
    yoe = entities.get("yoe", 5)
    salary = get_salary_reality(role, yoe, entities.get("city", "Bengaluru"), current_ctc=entities.get("ctc"))
    context_parts.append(
        f"Salary data for {role} ({yoe} YOE): median ₹{salary.p50}L, p75 ₹{salary.p75}L, "
        f"confidence {salary.confidence}, n={salary.sample_size}."
    )
    citations.append(AdvisorCitation("salary", "Salary Reality Engine", "/tools/salary-reality-engine/"))

    # Company data
    company_name = entities.get("company")
    company = None
    if company_name:
        company = Company.objects.filter(name__icontains=company_name).first()
        if company:
            context_parts.append(f"{company.name}: score {company.overall_score}, sector {company.sector}.")
            citations.append(AdvisorCitation("company", company.name, f"/companies/{company.slug}/"))

    # Layoff signals
    if company_name:
        reports = LayoffReport.objects.filter(company_name__icontains=company_name).order_by("-created_at")[:3]
        if reports:
            statuses = ", ".join(r.get_status_display() for r in reports)
            context_parts.append(f"Recent layoff signals for {company_name}: {statuses}.")
            citations.append(AdvisorCitation("layoff", "Layoff Radar", "/layoff-radar/"))

    # Market index
    snap = CareerRealityIndexSnapshot.objects.order_by("-month_date").first()
    if snap:
        context_parts.append(
            f"Career Reality Index: salary pressure {snap.salary_pressure}, "
            f"switch difficulty {snap.switch_difficulty}, layoff risk {snap.layoff_risk}."
        )
        citations.append(AdvisorCitation("index", "Career Reality Index", "/career-reality-index/"))

    # Relevant article
    article = Article.objects.filter(status="published", title__icontains="salary").first()
    if not article:
        article = Article.objects.filter(status="published").order_by("-published_at").first()
    if article:
        context_parts.append(f"Editorial: {article.title}")
        citations.append(AdvisorCitation("article", article.title, article.get_absolute_url()))

    return "\n".join(context_parts), citations


def answer_career_question(question: str) -> AdvisorAnswer:
    """Generate evidence-backed answer using engines + optional LLM."""
    entities = _parse_entities(question)
    context, citations = _retrieve_context(question, entities)
    engines_used = ["salary_reality"]

    # Structured analysis for offer comparison questions
    if entities.get("offer_ctc") and entities.get("ctc"):
        current = OfferInput(
            label="Current",
            company_name=entities.get("company", "Current Co"),
            company=Company.objects.filter(name__icontains=entities.get("company", "")).first() if entities.get("company") else None,
            role=entities["role"],
            ctc=entities["ctc"],
            city=entities.get("city", "Bengaluru"),
        )
        offer = OfferInput(
            label="New Offer",
            company_name="Startup" if entities.get("offer_type") == "startup" else "New Company",
            company=None,
            role=entities["role"],
            ctc=entities["offer_ctc"],
            city=entities.get("city", "Bengaluru"),
            wlb_rating=3 if entities.get("offer_type") == "startup" else 4,
        )
        comparison = compare_offers(current, offer, entities.get("yoe", 5))
        engines_used.append("offer_analyzer")
        answer = (
            f"{comparison.verdict_label}. "
            + " ".join(comparison.reasoning[:2])
            + f" Current effective comp ~₹{comparison.offer_a.total_comp}L vs offer ~₹{comparison.offer_b.total_comp}L."
        )
        return AdvisorAnswer(answer=answer, citations=citations, engines_used=engines_used)

    # Stay/switch style questions
    if any(w in question.lower() for w in ["should i", "switch", "stay", "take", "leave"]):
        company = None
        if entities.get("company"):
            company = Company.objects.filter(name__icontains=entities["company"]).first()
        svs = analyze_stay_vs_switch(
            role=entities["role"],
            yoe=entities.get("yoe", 5),
            city=entities.get("city", "Bengaluru"),
            company_type=entities.get("company_type", "service"),
            current_ctc=entities.get("ctc", 15),
            company=company,
            has_offer=bool(entities.get("offer_ctc")),
            offer_ctc=entities.get("offer_ctc"),
        )
        engines_used.append("stay_vs_switch")
        answer = (
            f"{svs.recommendation_label}. "
            + " ".join(svs.financial_reasons[:1] + svs.career_reasons[:1])
        )
        return AdvisorAnswer(answer=answer, citations=citations, engines_used=engines_used)

    # Default: salary-focused answer + optional LLM
    ctc = entities.get("ctc")
    salary = get_salary_reality(
        entities["role"], entities.get("yoe", 5), entities.get("city", "Bengaluru"),
        current_ctc=ctc,
    )
    if ctc:
        answer = (
            f"At ₹{ctc}L with {entities.get('yoe', 5)} YOE as {entities['role']}, "
            f"you're at the {salary.percentile or 'unknown'}th percentile. "
            f"Market median is ₹{salary.p50}L; realistic switch target is ₹{salary.realistic_next}L. "
            f"Label: {salary.pay_label or 'insufficient data'}."
        )
    else:
        answer = (
            f"For {entities['role']} with {entities.get('yoe', 5)} YOE in {entities.get('city', 'Bengaluru')}, "
            f"market range is ₹{salary.p25}–₹{salary.p75}L (median ₹{salary.p50}L)."
        )

    llm_answer = _llm_enhance(question, context, answer)
    if llm_answer:
        answer = llm_answer

    return AdvisorAnswer(answer=answer, citations=citations, engines_used=engines_used)


def _llm_enhance(question: str, context: str, base_answer: str) -> str | None:
    from django.conf import settings
    api_key = getattr(settings, "OPENAI_API_KEY", "")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": (
                    "You are CareerReality's career advisor for Indian tech professionals. "
                    "Answer in 3-4 sentences using ONLY the provided data. Be direct. Use INR. "
                    "Cite numbers from the context. Do not invent data."
                )},
                {"role": "user", "content": f"Question: {question}\n\nData:\n{context}\n\nDraft: {base_answer}"},
            ],
            max_tokens=200,
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None
