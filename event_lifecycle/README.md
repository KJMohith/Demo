# Event Lifecycle & Certification System

Clean Django dashboard for event management with user registration, duplicate transaction prevention, QR code support, automatic registration emails, AJAX attendance toggling, feedback, and conditional certificate PDF download.

## Folder Structure

```text
event_lifecycle/
├── events/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── utils.py
│   ├── validators.py
├── templates/
│   ├── base.html
│   ├── events/register.html
│   ├── events/dashboard.html
│   ├── events/feedback.html
├── static/js/ajax_toggle.js
├── media/receipts/
├── requirements.txt
├── README.md
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Features Implemented

- Admin-style dashboard to add users and events.
- Real-time stats counter (participants/events/attendance/feedback).
- AJAX attendance toggle + live table refresh without manual page refresh.
- Transaction ID uniqueness validation (duplicate blocked).
- Receipt and photo validation (size/type errors shown immediately).
- Registration confirmation email (console backend by default).
- QR code shown per registered user (links to certificate route).
- Feedback capture and conditional PDF certificate download.
- Mobile responsive layout using Bootstrap 5.

## Eligibility Rule

Certificate PDF is downloadable only when:
- `attendance = True`
- `feedback_given = True`

Else server returns HTTP 403.

## CO Mapping

- **CO1: URL routing** — URLs cover register, dashboard APIs, feedback, and certificate.
- **CO2: Models + Forms validation** — duplicate transaction ID prevention and file/rating validation.
- **CO3: Template inheritance** — pages inherit from `base.html`.
- **CO4: PDF generation** — ReportLab used in `events/utils.py`.
- **CO5: AJAX attendance** — Fetch API updates attendance and dashboard data.

## SDG Justification (150 words)

This project supports transparent and fair digital event administration by creating a traceable lifecycle for every participant. Registration enforces unique transaction IDs and strict file validation, which reduces fraudulent or duplicated submissions and protects process integrity. The dashboard offers real-time counters and no-refresh updates, helping administrators make timely, evidence-based decisions without relying on manual records. QR mapping for each participant improves verification and discoverability of certificate records. Feedback collection ensures that participant input is part of the completion process, supporting continuous quality improvement. Certificate issuance is rule-based and consistent for all users, which strengthens fairness and prevents arbitrary decisions. Automated confirmation emails improve communication reliability and reduce administrative delays. By digitizing event operations—registration, tracking, feedback, and certification—the system minimizes paperwork, improves operational efficiency, and builds an auditable, accountable framework for academic or institutional events. This aligns with responsible innovation, inclusive digital governance, and sustainable modernization of educational administration processes.
