# Event Lifecycle & Certification System

A Django project that manages participant registration, attendance, feedback, and certificate generation with strict eligibility rules.

## Folder Structure

```text
event_lifecycle/
├── event_lifecycle/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── events/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── utils.py
│   ├── validators.py
│   └── views.py
├── templates/
│   ├── base.html
│   └── events/
│       ├── dashboard.html
│       ├── feedback.html
│       └── register.html
├── static/js/ajax_toggle.js
├── media/receipts/
├── manage.py
├── requirements.txt
└── README.md
```

## Installation Steps

1. Create and activate virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start server:
   ```bash
   python manage.py runserver
   ```

## Run Instructions

- Registration: `http://127.0.0.1:8000/`
- Dashboard: `http://127.0.0.1:8000/dashboard/`
- Feedback: available from dashboard action button
- Certificate: available from dashboard action button; returns PDF only when eligible.

## Core Flow

Registration (valid transaction + valid receipt) → attendance toggle via AJAX → feedback submission → conditional PDF certificate.

Certificate eligibility requires all to be true:

- `transaction_verified`
- `attendance`
- `feedback_given`

Otherwise, HTTP 403 is returned.

## CO Mapping

- **CO1: URL routing** — project/app URLs route registration, dashboard, feedback, attendance toggle, and certificate endpoints.
- **CO2: Models + Forms validation** — model and forms enforce unique transaction IDs, receipt constraints, and rating constraints.
- **CO3: Template inheritance** — all page templates inherit from `base.html`.
- **CO4: PDF generation** — `events/utils.py` uses ReportLab to render certificate PDF.
- **CO5: AJAX attendance** — `static/js/ajax_toggle.js` uses Fetch API for no-refresh attendance toggling.

## SDG Justification (150 words)

This system supports transparent and fair academic/event administration by ensuring that certificates are generated only when objective participation criteria are met. Every participant must complete registration with a unique transaction ID and receipt validation, reducing duplicate or fraudulent enrollment. Attendance tracking is handled consistently from a central dashboard, and immediate AJAX updates reduce manual errors while preserving a clear status trail. Feedback collection ensures participant reflection and quality assurance before certification, helping organizers improve delivery and accountability. The eligibility rule (`transaction_verified && attendance && feedback_given`) applies equally to every participant, improving fairness and minimizing bias in certificate issuance. Digital records for transactions, attendance, and feedback provide auditable evidence for decisions, which strengthens trust among learners, institutions, and organizers. By replacing paper-heavy workflows with structured digital processes, the project also promotes efficient, inclusive, and scalable academic management aligned with responsible innovation and institutional transparency goals.
