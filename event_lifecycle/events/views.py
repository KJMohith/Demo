from django.conf import settings
from django.core.mail import send_mail
from django.http import FileResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import EventForm, FeedbackForm, MarksForm, RegistrationForm
from .models import Event, Participant
from .utils import generate_certificate_pdf, generate_qr_data


def _send_registration_email(participant, request):
    certificate_url = request.build_absolute_uri(reverse('certificate', args=[participant.certificate_hash]))
    send_mail(
        subject='Event Registration Confirmation',
        message=(
            f'Hi {participant.name},\n\n'
            f'You are registered successfully.\n'
            f'Your transaction ID: {participant.transaction_id}\n'
            f'Certificate link (active after eligibility): {certificate_url}\n'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[participant.email],
        fail_silently=True,
    )


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save()
            _send_registration_email(participant, request)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'events/register.html', {'form': form})


def dashboard(request):
    participants = Participant.objects.all()
    events = Event.objects.all()
    participant_form = RegistrationForm()
    event_form = EventForm()

    for participant in participants:
        participant.qr_data = generate_qr_data(
            request.build_absolute_uri(reverse('certificate', args=[participant.certificate_hash]))
        )

    context = {
        'participants': participants,
        'events': events,
        'participant_form': participant_form,
        'event_form': event_form,
    }
    return render(request, 'events/dashboard.html', context)


@require_POST
def update_marks(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    form = MarksForm(request.POST, instance=participant)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    form.save(update_fields=['marks'])
    return JsonResponse({'message': 'Marks updated successfully.'})


@require_POST
def add_participant(request):
    form = RegistrationForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    participant = form.save()
    _send_registration_email(participant, request)
    return JsonResponse({'message': 'Participant added successfully.'})


@require_POST
def add_event(request):
    form = EventForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    event = form.save()
    return JsonResponse(
        {
            'message': 'Event added successfully.',
            'event': {
                'id': event.id,
                'title': event.title,
                'event_date': str(event.event_date),
                'description': event.description or 'No description',
            },
        }
    )


@require_POST
def delete_participant(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    participant.delete()
    return JsonResponse({'message': 'Student deleted successfully.'})


@require_POST
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return JsonResponse({'message': 'Event deleted successfully.'})


@require_POST
def toggle_attendance(request, pk):
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'AJAX request required.'}, status=400)

    participant = get_object_or_404(Participant, pk=pk)
    participant.attendance = not participant.attendance
    participant.save(update_fields=['attendance'])
    return JsonResponse({'attendance': participant.attendance})


def feedback(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            participant.rating = form.cleaned_data['rating']
            participant.feedback_text = form.cleaned_data['comment']
            participant.feedback_given = True
            participant.save(update_fields=['rating', 'feedback_text', 'feedback_given'])
            return redirect('dashboard')
    else:
        form = FeedbackForm(initial={'rating': participant.rating})

    return render(request, 'events/feedback.html', {'form': form, 'participant': participant})


def dashboard_stats(request):
    return JsonResponse(
        {
            'participants': Participant.objects.count(),
            'events': Event.objects.count(),
            'attended': Participant.objects.filter(attendance=True).count(),
            'feedback': Participant.objects.filter(feedback_given=True).count(),
        }
    )


def participant_rows(request):
    participants = Participant.objects.all()
    for participant in participants:
        participant.qr_data = generate_qr_data(
            request.build_absolute_uri(reverse('certificate', args=[participant.certificate_hash]))
        )
    html = render_to_string('events/participant_rows.html', {'participants': participants}, request=request)
    return JsonResponse({'html': html})


def certificate(request, hash):
    participant = get_object_or_404(Participant, certificate_hash=hash)
    if not participant.is_eligible():
        return HttpResponseForbidden('Certificate is not available. Eligibility requirements are not met.')

    pdf_buffer = generate_certificate_pdf(participant)
    filename = f'certificate_{participant.name.replace(" ", "_")}.pdf'
    return FileResponse(pdf_buffer, as_attachment=True, filename=filename, content_type='application/pdf')
