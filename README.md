# Computer Maintenance Expert System

This project is a rule-based expert system for home-user computer maintenance. It covers both hardware and software issues and uses a backward-chaining inference engine implemented entirely in Python.

## Features

- Structured knowledge base for hardware and software maintenance problems
- Backward-chaining rule engine that asks only the questions needed to prove a diagnosis
- Desktop user interface built with `tkinter`
- Web user interface built with `Flask`
- Bilingual user interface and knowledge presentation in English and French
- Safe recommendations aimed at home users, with escalation guidance for risky cases

## Project Structure

```text
.
├── expert_system
│   ├── __init__.py
│   ├── engine.py
|   ├── i18n.py
│   ├── knowledge_base.py
│   ├── models.py
│   ├── static
│   ├── templates
│   ├── ui.py
│   └── web.py
├── app.py
├── main.py
├── Procfile
├── requirements.txt
└── README.md
```

## Run

Use Python 3.10 or newer:

```bash
python3 main.py
```

That starts the desktop `tkinter` application.

For the web version:

```bash
python3 app.py
```

Then open `http://127.0.0.1:5000` in your browser.

You can also use Flask's development server explicitly:

```bash
flask --app app run --debug
```

## Deploy The Web Version

Install the web dependencies:

```bash
pip install -r requirements.txt
```

The repository includes:

- `requirements.txt` for Python dependencies
- `Procfile` for platforms that launch `gunicorn`
- `app.py` as the WSGI entry point

For production hosting, point your platform to:

```bash
gunicorn app:app
```

## How It Works

1. The user selects a symptom path such as "Computer does not turn on" or "System is slow or freezes".
2. The backward-chaining engine starts from the candidate diagnoses linked to that symptom path.
3. The engine proves or rejects rules by asking only the missing facts required by each rule.
4. When a rule is fully proved, the UI shows the diagnosis, supporting evidence, safe actions, and escalation advice.

## Knowledge Base

The current knowledge base includes:

- Hardware: power, boot, display, overheating, peripheral, and port issues
- Software: performance, network, application, security, login, and update issues
