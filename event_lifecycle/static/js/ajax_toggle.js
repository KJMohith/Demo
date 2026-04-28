// ── CSRF ──────────────────────────────────────────────────────────────────────
function getCookie(name) {
  let val = null;
  if (document.cookie) {
    for (const raw of document.cookie.split(';')) {
      const c = raw.trim();
      if (c.startsWith(name + '=')) { val = decodeURIComponent(c.slice(name.length + 1)); break; }
    }
  }
  return val;
}
const csrfToken = getCookie('csrftoken');

// ── STATS ─────────────────────────────────────────────────────────────────────
async function fetchStats() {
  const r = await fetch('/dashboard/stats/');
  if (!r.ok) return;
  const d = await r.json();
  document.getElementById('count-participants').textContent = d.participants;
  document.getElementById('count-events').textContent = d.events;
  document.getElementById('count-attended').textContent = d.attended;
  document.getElementById('count-feedback').textContent = d.feedback;
  const badge = document.getElementById('participant-count-badge');
  if (badge) badge.textContent = d.participants + ' registered';
}

// ── PARTICIPANT ROWS ──────────────────────────────────────────────────────────
async function fetchParticipantRows() {
  const r = await fetch('/dashboard/participants/');
  if (!r.ok) return;
  const d = await r.json();
  document.getElementById('participant-table-body').innerHTML = d.html;
}

// ── ERRORS ────────────────────────────────────────────────────────────────────
function showErrors(id, errors) {
  const el = document.getElementById(id);
  el.textContent = Object.entries(errors).map(([k, v]) => k + ': ' + v.join(', ')).join(' | ');
}

// ── ADD STUDENT ───────────────────────────────────────────────────────────────
const participantForm = document.getElementById('participant-form');
if (participantForm) {
  participantForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    document.getElementById('participant-errors').textContent = '';
    const r = await fetch('/dashboard/add-user/', {
      method: 'POST',
      body: new FormData(participantForm),
      headers: { 'X-CSRFToken': csrfToken },
    });
    if (!r.ok) {
      const d = await r.json();
      showErrors('participant-errors', d.errors || { error: ['Unable to add student.'] });
      showToast('Failed to add student', 'error');
      return;
    }
    participantForm.reset();
    await fetchParticipantRows();
    await fetchStats();
    showToast('Student added successfully!');
  });
}

// ── ADD EVENT ─────────────────────────────────────────────────────────────────
const eventForm = document.getElementById('event-form');
if (eventForm) {
  eventForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    document.getElementById('event-errors').textContent = '';
    const r = await fetch('/dashboard/add-event/', {
      method: 'POST',
      body: new FormData(eventForm),
      headers: { 'X-CSRFToken': csrfToken },
    });
    if (!r.ok) {
      const d = await r.json();
      showErrors('event-errors', d.errors || { error: ['Unable to add event.'] });
      showToast('Failed to add event', 'error');
      return;
    }
    const d = await r.json();
    eventForm.reset();
    const div = document.createElement('div');
    div.className = 'event-item';
    div.dataset.eventId = d.event.id;
    div.innerHTML = `
      <div style="display:flex;gap:.6rem;align-items:flex-start;flex:1;min-width:0;">
        <span class="event-dot" style="margin-top:6px;"></span>
        <div style="min-width:0;">
          <div style="font-weight:700;font-size:.85rem;color:var(--ink);">${d.event.title}</div>
          <div style="font-size:.75rem;color:var(--ink-3);margin-top:1px;">${d.event.event_date} · ${d.event.description}</div>
        </div>
      </div>
      <button class="btn btn-sm btn-outline-danger delete-event flex-shrink-0"
              data-url="/dashboard/delete-event/${d.event.id}/">
        <i class="bi bi-trash3"></i>
      </button>`;
    document.getElementById('event-list').prepend(div);
    await fetchStats();
    showToast('Event "' + d.event.title + '" added!');
  });
}

// ── EVENT DELEGATION ──────────────────────────────────────────────────────────
document.addEventListener('click', async (e) => {
  // Toggle attendance
  const toggleBtn = e.target.closest('.attendance-toggle');
  if (toggleBtn) {
    const r = await fetch(toggleBtn.dataset.url, {
      method: 'POST',
      headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrfToken },
    });
    if (!r.ok) return;
    const d = await r.json();
    await fetchParticipantRows();
    await fetchStats();
    showToast('Attendance ' + (d.attendance ? 'marked ✓' : 'unmarked'));
    return;
  }

  // Delete student
  const delStudent = e.target.closest('.delete-student');
  if (delStudent) {
    if (!confirm('Delete this participant?')) return;
    const r = await fetch(delStudent.dataset.url, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
    });
    if (!r.ok) return;
    await fetchParticipantRows();
    await fetchStats();
    showToast('Participant removed.');
    return;
  }

  // Delete event
  const delEvent = e.target.closest('.delete-event');
  if (delEvent) {
    if (!confirm('Delete this event?')) return;
    const r = await fetch(delEvent.dataset.url, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
    });
    if (!r.ok) return;
    delEvent.closest('[data-event-id]')?.remove();
    await fetchParticipantRows();
    await fetchStats();
    showToast('Event deleted.');
    return;
  }
});

// ── MARKS ─────────────────────────────────────────────────────────────────────
document.addEventListener('submit', async (e) => {
  const form = e.target.closest('.marks-form');
  if (!form) return;
  e.preventDefault();
  const r = await fetch(form.dataset.url, {
    method: 'POST',
    body: new FormData(form),
    headers: { 'X-CSRFToken': csrfToken },
  });
  if (!r.ok) { showToast('Failed to save marks', 'error'); return; }
  await fetchParticipantRows();
  await fetchStats();
  showToast('Marks saved!');
});

// ── INIT ──────────────────────────────────────────────────────────────────────
fetchStats();
setInterval(fetchStats, 5000);