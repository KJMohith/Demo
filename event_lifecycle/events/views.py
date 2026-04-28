from django.http import FileResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import FeedbackForm, RegistrationForm
from .models import Participant
from .utils import generate_certificate_pdf


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.transaction_verified = True
            participant.save()
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'events/register.html', {'form': form})


def dashboard(request):
    participants = Participant.objects.all().order_by('-id')
    return render(request, 'events/dashboard.html', {'participants': participants})


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


def certificate(request, hash):
    participant = get_object_or_404(Participant, certificate_hash=hash)
    if not participant.is_eligible():
        return HttpResponseForbidden('Certificate is not available. Eligibility requirements are not met.')

    pdf_buffer = generate_certificate_pdf(participant)
    filename = f'certificate_{participant.name.replace(" ", "_")}.pdf'
    return FileResponse(pdf_buffer, as_attachment=True, filename=filename, content_type='application/pdf')
