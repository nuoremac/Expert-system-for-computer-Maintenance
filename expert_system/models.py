from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    fact: str
    prompt: str
    help_text: str = ""


@dataclass(frozen=True)
class Rule:
    id: str
    conclusion: str
    premises: tuple[str, ...]
    explanation: str


@dataclass(frozen=True)
class Diagnosis:
    id: str
    title: str
    category: str
    summary: str
    recommendations: tuple[str, ...]
    escalation: tuple[str, ...]


@dataclass(frozen=True)
class SymptomPath:
    id: str
    category: str
    label: str
    description: str
    goals: tuple[str, ...]


@dataclass(frozen=True)
class KnowledgeBase:
    questions: dict[str, Question]
    rules: tuple[Rule, ...]
    diagnoses: dict[str, Diagnosis]
    symptom_paths: tuple[SymptomPath, ...]
