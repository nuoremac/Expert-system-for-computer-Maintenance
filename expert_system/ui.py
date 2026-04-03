from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from .engine import (
    BackwardChainingEngine,
    DiagnosisOutcome,
    ExpertSession,
    QuestionOutcome,
    UnresolvedOutcome,
)
from .i18n import Language, translate
from .knowledge_base import KNOWLEDGE_BASE


CATEGORY_LABELS = {"hardware": "Hardware", "software": "Software"}
ANSWER_LABELS = {True: "Yes", False: "No", None: "Not sure"}


class ExpertSystemApp(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master, padding=18)
        self.master = master
        self.engine = BackwardChainingEngine(KNOWLEDGE_BASE)
        self.session: ExpertSession | None = None
        self.last_outcome: DiagnosisOutcome | UnresolvedOutcome | None = None
        self.current_symptom_paths = []

        self.language_var = tk.StringVar(value="en")
        self.category_var = tk.StringVar(value="hardware")
        self.device_type_var = tk.StringVar(value="laptop")
        self.status_var = tk.StringVar(value="")
        self.question_var = tk.StringVar(value="")
        self.help_var = tk.StringVar(value="")
        self.path_description_var = tk.StringVar(value="")

        self._configure_style()
        self._build_layout()
        self._populate_symptom_paths()
        self._apply_language()

    def _configure_style(self) -> None:
        self.master.title(self._t("Computer Maintenance Expert System"))
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = min(1180, max(940, screen_width - 80))
        window_height = min(760, max(620, screen_height - 120))
        self.master.geometry(f"{window_width}x{window_height}")
        self.master.minsize(940, 620)
        self.master.configure(bg="#f4ecdf")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("App.TFrame", background="#f4ecdf")
        style.configure("Card.TFrame", background="#fff8ef", relief="flat")
        style.configure("Header.TFrame", background="#17324d")
        style.configure(
            "HeaderTitle.TLabel",
            background="#17324d",
            foreground="#fff6e9",
            font=("Helvetica", 24, "bold"),
        )
        style.configure(
            "HeaderSubtitle.TLabel",
            background="#17324d",
            foreground="#d6e4ef",
            font=("Helvetica", 11),
        )
        style.configure(
            "Section.TLabel",
            background="#fff8ef",
            foreground="#17324d",
            font=("Helvetica", 13, "bold"),
        )
        style.configure(
            "Body.TLabel",
            background="#fff8ef",
            foreground="#283c4f",
            font=("Helvetica", 11),
        )
        style.configure(
            "Status.TLabel",
            background="#f4ecdf",
            foreground="#7a3f12",
            font=("Helvetica", 11, "italic"),
        )
        style.configure(
            "Accent.TButton",
            font=("Helvetica", 11, "bold"),
            padding=(14, 10),
            background="#c65d2d",
            foreground="#fffaf4",
            borderwidth=0,
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#ab4f24"), ("disabled", "#d6b7a4")],
            foreground=[("disabled", "#fffaf4")],
        )
        style.configure(
            "Secondary.TButton",
            font=("Helvetica", 10),
            padding=(12, 9),
            background="#ebe2d4",
            foreground="#17324d",
        )
        style.configure(
            "Answer.TButton",
            font=("Helvetica", 11, "bold"),
            padding=(12, 12),
            background="#2f6e73",
            foreground="#ffffff",
            borderwidth=0,
        )
        style.map(
            "Answer.TButton",
            background=[("active", "#275d61"), ("disabled", "#b4cdcf")],
            foreground=[("disabled", "#f7fbfb")],
        )
        style.configure("TRadiobutton", background="#fff8ef", foreground="#283c4f")
        style.configure("TCombobox", padding=6)

    def _build_layout(self) -> None:
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ttk.Frame(self, style="Header.TFrame", padding=(24, 18))
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        self.header_title_label = ttk.Label(header, text="", style="HeaderTitle.TLabel")
        self.header_title_label.grid(row=0, column=0, sticky="w")
        self.header_subtitle_label = ttk.Label(header, text="", style="HeaderSubtitle.TLabel")
        self.header_subtitle_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        ttk.Label(self, textvariable=self.status_var, style="Status.TLabel").grid(
            row=1, column=0, sticky="ew", pady=(14, 12)
        )

        body = ttk.Frame(self, style="App.TFrame")
        body.grid(row=2, column=0, sticky="nsew")
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=0)
        body.grid_columnconfigure(1, weight=1)

        sidebar = ttk.Frame(body, style="Card.TFrame", padding=18)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_rowconfigure(8, weight=1)

        self.setup_label = ttk.Label(sidebar, text="", style="Section.TLabel")
        self.setup_label.grid(row=0, column=0, sticky="w")

        self.language_label = ttk.Label(
            sidebar,
            text="",
            style="Body.TLabel",
            wraplength=280,
        )
        self.language_label.grid(row=1, column=0, sticky="w", pady=(12, 6))

        language_frame = ttk.Frame(sidebar, style="Card.TFrame")
        language_frame.grid(row=2, column=0, sticky="ew")
        self.language_en_button = ttk.Radiobutton(
            language_frame,
            text="",
            value="en",
            variable=self.language_var,
            command=self._apply_language,
        )
        self.language_en_button.grid(row=0, column=0, sticky="w", pady=2, padx=(0, 16))
        self.language_fr_button = ttk.Radiobutton(
            language_frame,
            text="",
            value="fr",
            variable=self.language_var,
            command=self._apply_language,
        )
        self.language_fr_button.grid(row=0, column=1, sticky="w", pady=2)

        self.issue_type_label = ttk.Label(
            sidebar,
            text="",
            style="Body.TLabel",
            wraplength=280,
        )
        self.issue_type_label.grid(row=3, column=0, sticky="w", pady=(16, 6))

        radio_frame = ttk.Frame(sidebar, style="Card.TFrame")
        radio_frame.grid(row=4, column=0, sticky="ew")
        self.hardware_radio = ttk.Radiobutton(
            radio_frame,
            text="",
            value="hardware",
            variable=self.category_var,
            command=self._populate_symptom_paths,
        )
        self.hardware_radio.grid(row=0, column=0, sticky="w", pady=2)
        self.software_radio = ttk.Radiobutton(
            radio_frame,
            text="",
            value="software",
            variable=self.category_var,
            command=self._populate_symptom_paths,
        )
        self.software_radio.grid(row=1, column=0, sticky="w", pady=2)

        self.device_type_label = ttk.Label(
            sidebar,
            text="",
            style="Body.TLabel",
            wraplength=280,
        )
        self.device_type_label.grid(row=5, column=0, sticky="w", pady=(16, 6))

        device_frame = ttk.Frame(sidebar, style="Card.TFrame")
        device_frame.grid(row=6, column=0, sticky="ew")
        self.device_laptop_button = ttk.Radiobutton(
            device_frame,
            text="",
            value="laptop",
            variable=self.device_type_var,
        )
        self.device_laptop_button.grid(row=0, column=0, sticky="w", pady=2, padx=(0, 12))
        self.device_desktop_button = ttk.Radiobutton(
            device_frame,
            text="",
            value="desktop",
            variable=self.device_type_var,
        )
        self.device_desktop_button.grid(row=0, column=1, sticky="w", pady=2, padx=(0, 12))
        self.device_unknown_button = ttk.Radiobutton(
            device_frame,
            text="",
            value="unknown",
            variable=self.device_type_var,
        )
        self.device_unknown_button.grid(row=0, column=2, sticky="w", pady=2)

        self.symptom_label = ttk.Label(
            sidebar,
            text="",
            style="Body.TLabel",
            wraplength=280,
        )
        self.symptom_label.grid(row=7, column=0, sticky="w", pady=(16, 6))

        symptom_frame = ttk.Frame(sidebar, style="Card.TFrame")
        symptom_frame.grid(row=8, column=0, sticky="nsew")
        symptom_frame.grid_rowconfigure(0, weight=1)
        symptom_frame.grid_columnconfigure(0, weight=1)

        self.symptom_listbox = tk.Listbox(
            symptom_frame,
            activestyle="none",
            bg="#f7efe3",
            fg="#20384b",
            font=("Helvetica", 11),
            highlightthickness=1,
            highlightbackground="#d8c5ae",
            selectbackground="#c65d2d",
            selectforeground="#fffaf4",
            exportselection=False,
            width=34,
            height=8,
            relief="flat",
        )
        self.symptom_listbox.grid(row=0, column=0, sticky="nsew")
        self.symptom_listbox.bind("<<ListboxSelect>>", self._update_selected_path_description)
        symptom_scrollbar = ttk.Scrollbar(
            symptom_frame,
            orient="vertical",
            command=self.symptom_listbox.yview,
        )
        symptom_scrollbar.grid(row=0, column=1, sticky="ns")
        self.symptom_listbox.configure(yscrollcommand=symptom_scrollbar.set)

        ttk.Label(
            sidebar,
            textvariable=self.path_description_var,
            style="Body.TLabel",
            wraplength=280,
            justify="left",
        ).grid(row=9, column=0, sticky="ew", pady=(10, 16))

        action_frame = ttk.Frame(sidebar, style="Card.TFrame")
        action_frame.grid(row=10, column=0, sticky="ew")
        action_frame.grid_columnconfigure(0, weight=1)
        action_frame.grid_columnconfigure(1, weight=1)
        self.start_button = ttk.Button(
            action_frame,
            text="",
            style="Accent.TButton",
            command=self._start_session,
        )
        self.start_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.reset_button = ttk.Button(
            action_frame,
            text="",
            style="Secondary.TButton",
            command=self._reset_session,
        )
        self.reset_button.grid(row=0, column=1, sticky="ew")

        content = ttk.Frame(body, style="App.TFrame")
        content.grid(row=0, column=1, sticky="nsew")
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)

        question_card = ttk.Frame(content, style="Card.TFrame", padding=18)
        question_card.grid(row=0, column=0, sticky="ew")
        question_card.grid_columnconfigure(0, weight=1)

        self.current_prompt_label = ttk.Label(question_card, text="", style="Section.TLabel")
        self.current_prompt_label.grid(row=0, column=0, sticky="w")
        ttk.Label(
            question_card,
            textvariable=self.question_var,
            style="Body.TLabel",
            wraplength=760,
            justify="left",
        ).grid(row=1, column=0, sticky="ew", pady=(12, 8))
        ttk.Label(
            question_card,
            textvariable=self.help_var,
            style="Body.TLabel",
            wraplength=760,
            justify="left",
        ).grid(row=2, column=0, sticky="ew")

        answers = ttk.Frame(question_card, style="Card.TFrame")
        answers.grid(row=3, column=0, sticky="ew", pady=(16, 0))
        for column in range(3):
            answers.grid_columnconfigure(column, weight=1)

        self.answer_buttons: dict[bool | None, ttk.Button] = {}
        for idx, (label, value) in enumerate((("Yes", True), ("No", False), ("Not sure", None))):
            button = ttk.Button(
                answers,
                text=label,
                style="Answer.TButton",
                command=lambda answer=value: self._submit_answer(answer),
                state=tk.DISABLED,
            )
            button.grid(row=0, column=idx, sticky="ew", padx=(0, 10) if idx < 2 else 0)
            self.answer_buttons[value] = button

        self.notebook = ttk.Notebook(content)
        self.notebook.grid(row=1, column=0, sticky="nsew", pady=(16, 0))

        outcome_frame = ttk.Frame(self.notebook, style="Card.TFrame", padding=10)
        reasoning_frame = ttk.Frame(self.notebook, style="Card.TFrame", padding=10)
        outcome_frame.grid_rowconfigure(0, weight=1)
        outcome_frame.grid_columnconfigure(0, weight=1)
        reasoning_frame.grid_rowconfigure(0, weight=1)
        reasoning_frame.grid_columnconfigure(0, weight=1)

        self.outcome_text = ScrolledText(
            outcome_frame,
            wrap="word",
            font=("Consolas", 11),
            bg="#f9f3ea",
            fg="#21384b",
            relief="flat",
            padx=12,
            pady=12,
        )
        self.outcome_text.grid(row=0, column=0, sticky="nsew")

        self.reasoning_text = ScrolledText(
            reasoning_frame,
            wrap="word",
            font=("Consolas", 10),
            bg="#f9f3ea",
            fg="#21384b",
            relief="flat",
            padx=12,
            pady=12,
        )
        self.reasoning_text.grid(row=0, column=0, sticky="nsew")

        self.notebook.add(outcome_frame, text="")
        self.notebook.add(reasoning_frame, text="")

    @property
    def language(self) -> Language:
        return self.language_var.get()  # type: ignore[return-value]

    def _t(self, text: str, **kwargs: object) -> str:
        return translate(text, self.language, **kwargs)

    def _apply_language(self) -> None:
        selected_path_id = self._selected_path_id()
        self.master.title(self._t("Computer Maintenance Expert System"))
        self.header_title_label.configure(text=self._t("Computer Maintenance Expert System"))
        self.header_subtitle_label.configure(
            text=self._t("Hardware and software diagnosis")
        )
        self.setup_label.configure(text=self._t("Diagnosis Setup"))
        self.language_label.configure(text=self._t("Language"))
        self.language_en_button.configure(text=self._t("English"))
        self.language_fr_button.configure(text=self._t("French"))
        self.issue_type_label.configure(text=self._t("1. Pick the broad issue type."))
        self.hardware_radio.configure(text=self._category_label("hardware"))
        self.software_radio.configure(text=self._category_label("software"))
        self.device_type_label.configure(text=self._t("2. Select the computer type."))
        self.device_laptop_button.configure(text=self._t("Laptop"))
        self.device_desktop_button.configure(text=self._t("Desktop"))
        self.device_unknown_button.configure(text=self._t("Not sure"))
        self.symptom_label.configure(text=self._t("3. What is the issue?"))
        self.start_button.configure(text=self._t("Start Diagnosis"))
        self.reset_button.configure(text=self._t("Reset"))
        self.current_prompt_label.configure(text=self._t("Current Prompt"))
        for value, label in ANSWER_LABELS.items():
            self.answer_buttons[value].configure(text=self._t(label))
        self.notebook.tab(0, text=self._t("Outcome"))
        self.notebook.tab(1, text=self._t("Reasoning"))
        self._populate_symptom_paths(selected_path_id=selected_path_id)
        self._refresh_textual_state()

    def _selected_path_id(self) -> str | None:
        selection = self.symptom_listbox.curselection()
        if not selection or not self.current_symptom_paths:
            return None
        return self.current_symptom_paths[selection[0]].id

    def _category_label(self, category: str) -> str:
        return self._t(CATEGORY_LABELS[category])

    def _answer_label(self, value: bool | None) -> str:
        return self._t(ANSWER_LABELS[value])

    def _populate_symptom_paths(self, selected_path_id: str | None = None) -> None:
        self.current_symptom_paths = self.engine.symptom_paths_for_category(self.category_var.get())
        self.symptom_listbox.delete(0, tk.END)
        for symptom_path in self.current_symptom_paths:
            self.symptom_listbox.insert(tk.END, self._t(symptom_path.label))

        if self.current_symptom_paths:
            target_index = 0
            if selected_path_id is not None:
                for index, symptom_path in enumerate(self.current_symptom_paths):
                    if symptom_path.id == selected_path_id:
                        target_index = index
                        break
            self.symptom_listbox.selection_set(target_index)
            self._update_selected_path_description()
        else:
            self.path_description_var.set("")

    def _update_selected_path_description(self, _event: object | None = None) -> None:
        selection = self.symptom_listbox.curselection()
        if not selection:
            self.path_description_var.set("")
            return
        symptom_path = self.current_symptom_paths[selection[0]]
        self.path_description_var.set(self._t(symptom_path.description))

    def _refresh_textual_state(self) -> None:
        if self.session is None:
            self.status_var.set(
                self._t("Choose the issue category, pick the closest symptom, then start the diagnosis.")
            )
            self.question_var.set(self._t("The next question will appear here."))
            self.help_var.set(self._t("No active session yet."))
            self._set_answer_buttons_state(tk.DISABLED)
            self._set_text(
                self.outcome_text,
                self._t(
                    "No diagnosis yet.\n\nStart a session from the left panel to let the engine work backward from a chosen symptom."
                ),
            )
            self._set_text(self.reasoning_text, self._t("No facts collected yet."))
            return

        if self.session.current_question_id is not None:
            question = KNOWLEDGE_BASE.questions[self.session.current_question_id]
            self.status_var.set(
                self._t("Please answer the next question to continue.")
            )
            self.question_var.set(self._t(question.prompt))
            help_text = question.help_text or "Answer with the closest choice."
            self.help_var.set(self._t(help_text))
            self._set_answer_buttons_state(tk.NORMAL)
            self._set_text(self.outcome_text, self._format_session_overview())
            self._render_reasoning()
            return

        if isinstance(self.last_outcome, DiagnosisOutcome):
            self.status_var.set(self._t("Diagnosis completed."))
            self.question_var.set(self._t(self.last_outcome.diagnosis.title))
            self.help_var.set(
                self._t("A rule matched the selected symptom path. Review the safe steps below.")
            )
            self._set_answer_buttons_state(tk.DISABLED)
            self._set_text(self.outcome_text, self._format_diagnosis(self.last_outcome))
            self._render_reasoning()
            return

        if isinstance(self.last_outcome, UnresolvedOutcome):
            self.status_var.set(self._t("The current rules did not produce a confident diagnosis."))
            self.question_var.set(self._t("No rule was fully proved"))
            self.help_var.set(self._t("Try another symptom path if the current one is too broad."))
            self._set_answer_buttons_state(tk.DISABLED)
            self._set_text(self.outcome_text, self._format_unresolved(self.last_outcome))
            self._render_reasoning()
            return

        self.status_var.set(
            self._t(
                "Active diagnosis: {label}. Answer each question so the engine can prove or reject rules.",
                label=self._t(self.session.symptom_path.label),
            )
        )
        self.question_var.set(self._t("The next question will appear here."))
        self.help_var.set(self._t("No active session yet."))
        self._set_answer_buttons_state(tk.DISABLED)
        self._set_text(self.outcome_text, self._format_session_overview())
        self._render_reasoning()

    def _format_session_overview(self) -> str:
        if self.session is None:
            return self._t(
                "No diagnosis yet.\n\nStart a session from the left panel to let the engine work backward from a chosen symptom."
            )
        return self._t(
            "Symptom path: {label}\nCategory: {category}\n\nThe system is evaluating candidate diagnoses.",
            label=self._t(self.session.symptom_path.label),
            category=self._category_label(self.session.symptom_path.category),
        )

    def _start_session(self) -> None:
        selection = self.symptom_listbox.curselection()
        if not selection:
            self.status_var.set(self._t("Select a symptom path before starting the diagnosis."))
            return

        symptom_path = self.current_symptom_paths[selection[0]]
        preset_answers: dict[str, bool] = {}
        device_type = self.device_type_var.get()
        if device_type == "laptop":
            preset_answers["is_laptop"] = True
        elif device_type == "desktop":
            preset_answers["is_laptop"] = False

        self.session = self.engine.start_session(symptom_path.id, preset_answers=preset_answers)
        self.last_outcome = None
        self.status_var.set(
            self._t(
                "Active diagnosis: {label}. Answer each question so the engine can prove or reject rules.",
                label=self._t(symptom_path.label),
            )
        )
        self._set_text(self.outcome_text, self._format_session_overview())
        self._render_reasoning()
        self._advance_session()

    def _reset_session(self) -> None:
        self.session = None
        self.last_outcome = None
        self.status_var.set(
            self._t("Choose the issue category, pick the closest symptom, then start the diagnosis.")
        )
        self.question_var.set(self._t("The next question will appear here."))
        self.help_var.set(self._t("No active session yet."))
        self._set_answer_buttons_state(tk.DISABLED)
        self._set_text(
            self.outcome_text,
            self._t(
                "No diagnosis yet.\n\nStart a session from the left panel to let the engine work backward from a chosen symptom."
            ),
        )
        self._set_text(self.reasoning_text, self._t("No facts collected yet."))

    def _advance_session(self) -> None:
        if self.session is None:
            return

        outcome = self.session.next_step()
        if isinstance(outcome, QuestionOutcome):
            self.last_outcome = None
            self.question_var.set(self._t(outcome.question.prompt))
            help_text = outcome.question.help_text or "Answer with the closest choice."
            self.help_var.set(self._t(help_text))
            self.status_var.set(
                self._t("Please answer the next question to continue.")
            )
            self._set_answer_buttons_state(tk.NORMAL)
            self._set_text(self.outcome_text, self._format_session_overview())
            self._render_reasoning()
            return

        self._set_answer_buttons_state(tk.DISABLED)
        if isinstance(outcome, DiagnosisOutcome):
            self.last_outcome = outcome
            self.question_var.set(self._t(outcome.diagnosis.title))
            self.help_var.set(
                self._t("A rule matched the selected symptom path. Review the safe steps below.")
            )
            self.status_var.set(self._t("Diagnosis completed."))
            self._set_text(self.outcome_text, self._format_diagnosis(outcome))
        elif isinstance(outcome, UnresolvedOutcome):
            self.last_outcome = outcome
            self.question_var.set(self._t("No rule was fully proved"))
            self.help_var.set(self._t("Try another symptom path if the current one is too broad."))
            self.status_var.set(self._t("The current rules did not produce a confident diagnosis."))
            self._set_text(self.outcome_text, self._format_unresolved(outcome))

        self._render_reasoning()

    def _submit_answer(self, value: bool | None) -> None:
        if self.session is None or self.session.current_question_id is None:
            return
        self.session.answer_current_question(value)
        self._advance_session()

    def _format_diagnosis(self, outcome: DiagnosisOutcome) -> str:
        lines = [
            self._t("Diagnosis"),
            self._t(outcome.diagnosis.title),
            "",
            self._t("Simple explanation"),
            self._format_simple_explanation(outcome),
        ]

        lines.append("")
        lines.append(self._t("Safe actions"))
        for index, recommendation in enumerate(outcome.diagnosis.recommendations, start=1):
            lines.append(f"{index}. {self._t(recommendation)}")

        lines.append("")
        lines.append(self._t("Contact a technician:"))
        for item in outcome.diagnosis.escalation:
            lines.append(f"- {self._format_escalation_item(item)}")

        return "\n".join(lines)

    def _format_simple_explanation(self, outcome: DiagnosisOutcome) -> str:
        summary = self._t(outcome.diagnosis.summary)
        explanation = self._t(outcome.rule.explanation)
        if explanation.rstrip(".") == summary.rstrip("."):
            return summary
        return f"{explanation} {summary}"

    def _format_unresolved(self, outcome: UnresolvedOutcome) -> str:
        lines = [
            self._t("Diagnosis status: unresolved"),
            "",
            self._t(outcome.message),
            "",
            self._t("Recommended next steps:"),
            self._t("1. Start a new session and pick a more specific symptom path if one fits better."),
            self._t("2. Keep a note of the exact error messages, beep codes, or timing of the failure."),
            self._t(
                "3. If the system shows burning smells, repeated crashes, or data-loss risk, stop using it and contact a technician."
            ),
        ]
        return "\n".join(lines)

    def _format_escalation_item(self, item: str) -> str:
        rendered = self._t(item)

        if self.language == "fr":
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
                    if self.language == "fr":
                        return f"{target}{remainder}, contactez votre fournisseur d'acces"
                    return f"{target}{remainder}, contact your ISP"
                return f"{target}{remainder}"
        return rendered

    def _render_reasoning(self) -> None:
        if self.session is None or not self.session.answer_order:
            self._set_text(self.reasoning_text, self._t("No facts collected yet."))
            return

        lines = [
            self._t("Symptom path: {label}", label=self._t(self.session.symptom_path.label)),
            "",
            self._t("Collected facts:"),
        ]
        for fact in self.session.answer_order:
            answer = self.session.answers[fact]
            lines.append(f"- {self._fact_label(fact)} -> {self._answer_label(answer)}")

        self._set_text(self.reasoning_text, "\n".join(lines))

    def _fact_label(self, fact: str) -> str:
        question = KNOWLEDGE_BASE.questions.get(fact)
        if question is not None:
            return self._t(question.prompt)
        return self._t(fact.replace("_", " ").capitalize())

    def _set_answer_buttons_state(self, state: str) -> None:
        for button in self.answer_buttons.values():
            button.configure(state=state)

    @staticmethod
    def _set_text(widget: ScrolledText, content: str) -> None:
        widget.configure(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, content)
        widget.configure(state=tk.DISABLED)


def run_app() -> None:
    root = tk.Tk()
    app = ExpertSystemApp(root)
    app.grid(row=0, column=0, sticky="nsew")
    root.mainloop()
