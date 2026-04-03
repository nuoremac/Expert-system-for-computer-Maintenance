from __future__ import annotations

import os
from typing import Any, Literal
from urllib.parse import urlparse

from flask import Flask, flash, redirect, render_template, request, session, url_for

from .engine import BackwardChainingEngine, DiagnosisOutcome, ExpertSession, QuestionOutcome, UnresolvedOutcome
from .i18n import Language, translate
from .knowledge_base import KNOWLEDGE_BASE


FlowAnswer = Literal[True, False, None]

CATEGORY_LABELS = {"hardware": "Hardware", "software": "Software"}
DEVICE_LABELS = {"laptop": "Laptop", "desktop": "Desktop", "unknown": "Not sure"}
ANSWER_LABELS = {"yes": "Yes", "no": "No", "unknown": "Not sure"}

ENGINE = BackwardChainingEngine(KNOWLEDGE_BASE)


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "change-this-in-production")

    @app.context_processor
    def inject_template_helpers() -> dict[str, Any]:
        return {
            "t": lambda text, **kwargs: translate(text, current_language(), **kwargs),
            "language": current_language(),
            "category_label": category_label,
            "device_label": device_label,
            "diagnosis_label": diagnosis_label,
        }

    @app.get("/")
    def home() -> str:
        flow = load_flow()
        return render_dashboard(flow, request.path)

    @app.post("/start")
    def start_diagnosis() -> Any:
        category = request.form.get("category", "hardware")
        device_type = request.form.get("device_type", "unknown")
        symptom_path_id = request.form.get("symptom_path_id", "")

        if category not in CATEGORY_LABELS:
            category = "hardware"
        if device_type not in DEVICE_LABELS:
            device_type = "unknown"

        valid_paths = {path.id for path in ENGINE.symptom_paths_for_category(category)}
        if symptom_path_id not in valid_paths:
            flash(translate("Pick a valid symptom path before starting the diagnosis.", current_language()))
            return redirect(url_for("home"))

        save_flow(
            {
                "category": category,
                "device_type": device_type,
                "symptom_path_id": symptom_path_id,
                "answers": {},
                "answer_order": [],
            }
        )
        return redirect(url_for("diagnose"))

    @app.get("/diagnose")
    def diagnose() -> Any:
        flow = load_flow()
        if flow["symptom_path_id"] is None:
            flash(translate("Start a diagnosis session before answering questions.", current_language()))
            return redirect(url_for("home"))
        return render_dashboard(flow, request.path)

    @app.post("/answer")
    def answer_question() -> Any:
        flow = load_flow()
        if flow["symptom_path_id"] is None:
            flash(translate("Start a diagnosis session before answering questions.", current_language()))
            return redirect(url_for("home"))

        expert_session = build_session(flow)
        outcome = expert_session.next_step()
        if not isinstance(outcome, QuestionOutcome):
            return redirect(url_for("diagnose"))

        answer_token = request.form.get("answer", "")
        answer_value = parse_answer(answer_token)
        if answer_value == "invalid":
            flash(translate("Choose one of the proposed answers to continue.", current_language()))
            return redirect(url_for("diagnose"))

        fact = outcome.question.fact
        flow["answers"][fact] = answer_value
        if fact not in flow["answer_order"]:
            flow["answer_order"].append(fact)
        save_flow(flow)
        return redirect(url_for("diagnose"))

    @app.get("/restart")
    def restart() -> Any:
        session.pop("diagnosis_flow", None)
        flash(translate("A new diagnosis session is ready.", current_language()))
        return redirect(url_for("home"))

    @app.get("/language/<lang>")
    def set_language(lang: str) -> Any:
        if lang in {"en", "fr"}:
            session["language"] = lang
        destination = safe_next(request.args.get("next"))
        return redirect(destination)

    return app


def render_dashboard(flow: dict[str, Any], next_path: str) -> str:
    selected_path = selected_symptom_path(flow)
    visible_paths = ENGINE.symptom_paths_for_category(flow["category"])
    status_message = translate(
        "Choose the issue category, pick the closest symptom, then start the diagnosis.",
        current_language(),
    )
    question_text = translate("The backward-chaining interview will appear here.", current_language())
    help_text = translate("No active session yet.", current_language())
    outcome_text = translate(
        "No diagnosis yet.\n\nStart a session from the left panel to let the engine work backward from a chosen symptom.",
        current_language(),
    )
    answer_enabled = False

    if selected_path is not None:
        expert_session = build_session(flow)
        outcome = expert_session.next_step()

        if isinstance(outcome, QuestionOutcome):
            status_message = translate(
                "Please answer the next question to continue.",
                current_language(),
            )
            question_text = translate(outcome.question.prompt, current_language())
            help_text = translate(outcome.question.help_text or "Answer with the closest choice.", current_language())
            outcome_text = format_session_overview(expert_session)
            answer_enabled = True
        elif isinstance(outcome, DiagnosisOutcome):
            status_message = translate(
                "Diagnosis completed.",
                current_language(),
            )
            question_text = translate(outcome.diagnosis.title, current_language())
            help_text = translate(
                "A rule matched the selected symptom path. Review the safe steps below.",
                current_language(),
            )
            outcome_text = format_diagnosis_text(outcome)
        else:
            status_message = translate(
                "The current rules did not produce a confident diagnosis.",
                current_language(),
            )
            question_text = translate("No rule was fully proved", current_language())
            help_text = translate("Try another symptom path if the current one is too broad.", current_language())
            outcome_text = format_unresolved_text(outcome)

    return render_template(
        "dashboard.html",
        page_title=translate("Computer Maintenance Expert System", current_language()),
        selected_category=flow["category"],
        selected_device=flow["device_type"],
        selected_path_id=flow["symptom_path_id"],
        selected_path_description=translate(selected_path.description, current_language()) if selected_path else "",
        symptom_paths=visible_paths,
        symptom_paths_json={
            category: [
                {
                    "id": path.id,
                    "label": translate(path.label, current_language()),
                    "description": translate(path.description, current_language()),
                }
                for path in ENGINE.symptom_paths_for_category(category)
            ]
            for category in ("hardware", "software")
        },
        status_message=status_message,
        question_text=question_text,
        help_text=help_text,
        outcome_text=outcome_text,
        answer_enabled=answer_enabled,
        next_path=next_path,
    )


def current_language() -> Language:
    language = session.get("language", "en")
    if language in {"en", "fr"}:
        return language  # type: ignore[return-value]
    return "en"


def category_label(category: str) -> str:
    return translate(CATEGORY_LABELS[category], current_language())


def device_label(device_type: str) -> str:
    return translate(DEVICE_LABELS[device_type], current_language())


def diagnosis_label(diagnosis_id: str) -> str:
    return translate(KNOWLEDGE_BASE.diagnoses[diagnosis_id].title, current_language())


def selected_symptom_path(flow: dict[str, Any]):
    symptom_path_id = flow.get("symptom_path_id")
    if not symptom_path_id:
        return None
    return ENGINE.symptom_paths_by_id.get(symptom_path_id)


def load_flow() -> dict[str, Any]:
    flow = session.get("diagnosis_flow")
    if not isinstance(flow, dict):
        return {
            "category": "hardware",
            "device_type": "unknown",
            "symptom_path_id": None,
            "answers": {},
            "answer_order": [],
        }

    category = flow.get("category", "hardware")
    if category not in CATEGORY_LABELS:
        category = "hardware"

    device_type = flow.get("device_type", "unknown")
    if device_type not in DEVICE_LABELS:
        device_type = "unknown"

    symptom_path_id = flow.get("symptom_path_id")
    symptom_path = ENGINE.symptom_paths_by_id.get(symptom_path_id)
    if symptom_path is None or symptom_path.category != category:
        symptom_path_id = None

    normalized = {
        "category": category,
        "device_type": device_type,
        "symptom_path_id": symptom_path_id,
        "answers": dict(flow.get("answers", {})),
        "answer_order": list(flow.get("answer_order", [])),
    }
    return normalized


def save_flow(flow: dict[str, Any]) -> None:
    session["diagnosis_flow"] = flow
    session.modified = True


def build_session(flow: dict[str, Any]) -> ExpertSession:
    preset_answers: dict[str, FlowAnswer] = {}
    if flow["device_type"] == "laptop":
        preset_answers["is_laptop"] = True
    elif flow["device_type"] == "desktop":
        preset_answers["is_laptop"] = False

    expert_session = ENGINE.start_session(flow["symptom_path_id"], preset_answers=preset_answers)
    answers: dict[str, FlowAnswer] = flow["answers"]
    for fact in flow["answer_order"]:
        if fact == "is_laptop" and flow["device_type"] != "unknown":
            continue
        if fact in answers:
            expert_session.set_answer(fact, answers[fact])
    return expert_session


def format_session_overview(expert_session: ExpertSession) -> str:
    return translate(
        "Symptom path: {label}\nCategory: {category}\n\nThe system is evaluating candidate diagnoses.",
        current_language(),
        label=translate(expert_session.symptom_path.label, current_language()),
        category=category_label(expert_session.symptom_path.category),
    )


def format_diagnosis_text(outcome: DiagnosisOutcome) -> str:
    lines = [
        translate("Diagnosis", current_language()),
        translate(outcome.diagnosis.title, current_language()),
        "",
        translate("Simple explanation", current_language()),
        format_simple_explanation(outcome),
    ]

    lines.append("")
    lines.append(translate("Safe actions", current_language()))
    for index, recommendation in enumerate(outcome.diagnosis.recommendations, start=1):
        lines.append(f"{index}. {translate(recommendation, current_language())}")

    lines.append("")
    lines.append(translate("Contact a technician:", current_language()))
    for item in outcome.diagnosis.escalation:
        lines.append(f"- {format_escalation_item(item)}")

    return "\n".join(lines)


def format_unresolved_text(outcome: UnresolvedOutcome) -> str:
    lines = [
        translate("Diagnosis status: unresolved", current_language()),
        "",
        translate(outcome.message, current_language()),
        "",
        translate("Recommended next steps:", current_language()),
        translate("1. Start a new session and pick a more specific symptom path if one fits better.", current_language()),
        translate("2. Keep a note of the exact error messages, beep codes, or timing of the failure.", current_language()),
        translate(
            "3. If the system shows burning smells, repeated crashes, or data-loss risk, stop using it and contact a technician.",
            current_language(),
        ),
    ]
    return "\n".join(lines)


def format_simple_explanation(outcome: DiagnosisOutcome) -> str:
    summary = translate(outcome.diagnosis.summary, current_language())
    explanation = translate(outcome.rule.explanation, current_language())
    if explanation.rstrip(".") == summary.rstrip("."):
        return summary
    return f"{explanation} {summary}"


def format_escalation_item(item: str) -> str:
    rendered = translate(item, current_language())

    if current_language() == "fr":
        replacements = (
            ("Escaladez immediatement si ", "immediatement si "),
            ("Escaladez rapidement si ", "rapidement si "),
            ("Escaladez vers un technicien pour ", "pour "),
            ("Escaladez vers votre fournisseur d'acces si ", "si "),
            ("Escaladez pour ", "pour "),
            ("Escaladez si ", "si "),
        )
    else:
        replacements = (
            ("Escalate immediately if ", "immediately if "),
            ("Escalate quickly if ", "promptly if "),
            ("Escalate to a technician for ", "for "),
            ("Escalate to your ISP if ", "if "),
            ("Escalate for ", "for "),
            ("Escalate if ", "if "),
        )

    for source, target in replacements:
        if rendered.startswith(source):
            remainder = rendered[len(source):]
            if source in {"Escalate to your ISP if ", "Escaladez vers votre fournisseur d'acces si "}:
                if current_language() == "fr":
                    return f"{target}{remainder}, contactez votre fournisseur d'acces"
                return f"{target}{remainder}, contact your ISP"
            return f"{target}{remainder}"
    return rendered


def parse_answer(token: str) -> FlowAnswer | str:
    if token == "yes":
        return True
    if token == "no":
        return False
    if token == "unknown":
        return None
    return "invalid"


def safe_next(candidate: str | None) -> str:
    if not candidate:
        return url_for("home")
    parsed = urlparse(candidate)
    if parsed.netloc or parsed.scheme:
        return url_for("home")
    return candidate
