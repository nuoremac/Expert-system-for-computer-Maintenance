from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .models import Diagnosis, KnowledgeBase, Question, Rule, SymptomPath


class ProofState(Enum):
    PROVED = "proved"
    FAILED = "failed"
    NEEDS_INPUT = "needs_input"


@dataclass(frozen=True)
class ProofResult:
    state: ProofState
    question_id: Optional[str] = None
    supporting_facts: tuple[str, ...] = ()
    rule: Optional[Rule] = None


@dataclass(frozen=True)
class QuestionOutcome:
    question: Question


@dataclass(frozen=True)
class DiagnosisOutcome:
    diagnosis: Diagnosis
    rule: Rule
    supporting_facts: tuple[str, ...]


@dataclass(frozen=True)
class UnresolvedOutcome:
    message: str


class BackwardChainingEngine:
    def __init__(self, knowledge_base: KnowledgeBase) -> None:
        self.knowledge_base = knowledge_base
        self.rules_by_conclusion: dict[str, list[Rule]] = {}
        self.symptom_paths_by_id = {
            symptom_path.id: symptom_path for symptom_path in knowledge_base.symptom_paths
        }
        for rule in knowledge_base.rules:
            self.rules_by_conclusion.setdefault(rule.conclusion, []).append(rule)

    def symptom_paths_for_category(self, category: str) -> list[SymptomPath]:
        return [
            symptom_path
            for symptom_path in self.knowledge_base.symptom_paths
            if symptom_path.category == category
        ]

    def start_session(
        self,
        symptom_path_id: str,
        preset_answers: Optional[dict[str, Optional[bool]]] = None,
    ) -> "ExpertSession":
        symptom_path = self.symptom_paths_by_id[symptom_path_id]
        return ExpertSession(engine=self, symptom_path=symptom_path, preset_answers=preset_answers or {})


class ExpertSession:
    def __init__(
        self,
        engine: BackwardChainingEngine,
        symptom_path: SymptomPath,
        preset_answers: dict[str, Optional[bool]],
    ) -> None:
        self.engine = engine
        self.symptom_path = symptom_path
        self.answers: dict[str, Optional[bool]] = {}
        self.answer_order: list[str] = []
        self.current_question_id: Optional[str] = None
        for fact, value in preset_answers.items():
            self.set_answer(fact, value)

    def set_answer(self, fact: str, value: Optional[bool]) -> None:
        self.answers[fact] = value
        if fact not in self.answer_order:
            self.answer_order.append(fact)

    def answer_current_question(self, value: Optional[bool]) -> None:
        if self.current_question_id is None:
            return
        self.set_answer(self.current_question_id, value)
        self.current_question_id = None

    def next_step(self) -> QuestionOutcome | DiagnosisOutcome | UnresolvedOutcome:
        for goal in self.symptom_path.goals:
            result = self._prove(goal, trail=set())
            if result.state is ProofState.PROVED and result.rule is not None:
                diagnosis = self.engine.knowledge_base.diagnoses[goal]
                return DiagnosisOutcome(
                    diagnosis=diagnosis,
                    rule=result.rule,
                    supporting_facts=result.supporting_facts,
                )
            if result.state is ProofState.NEEDS_INPUT and result.question_id is not None:
                self.current_question_id = result.question_id
                return QuestionOutcome(self.engine.knowledge_base.questions[result.question_id])

        self.current_question_id = None
        return UnresolvedOutcome(
            message=(
                "The current rules did not prove a diagnosis with enough confidence. "
                "Use the safe checks already performed, then consider a technician or a more specific symptom path."
            )
        )

    def _prove(self, goal: str, trail: set[str]) -> ProofResult:
        if goal in trail:
            return ProofResult(state=ProofState.FAILED)

        if goal in self.answers:
            if self.answers[goal] is True:
                return ProofResult(state=ProofState.PROVED, supporting_facts=(goal,))
            return ProofResult(state=ProofState.FAILED)

        question = self.engine.knowledge_base.questions.get(goal)
        if question is not None:
            return ProofResult(state=ProofState.NEEDS_INPUT, question_id=goal)

        next_trail = set(trail)
        next_trail.add(goal)
        for rule in self.engine.rules_by_conclusion.get(goal, []):
            evidence: list[str] = []
            for premise in rule.premises:
                result = self._prove(premise, next_trail)
                if result.state is ProofState.NEEDS_INPUT:
                    return result
                if result.state is ProofState.FAILED:
                    break
                evidence.extend(result.supporting_facts)
            else:
                unique_evidence = tuple(dict.fromkeys(evidence))
                return ProofResult(
                    state=ProofState.PROVED,
                    supporting_facts=unique_evidence,
                    rule=rule,
                )

        return ProofResult(state=ProofState.FAILED)
