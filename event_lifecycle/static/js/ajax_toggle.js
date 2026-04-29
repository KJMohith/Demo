/* ═══════════════════════════════════════════════════════════════
   EventFlow  ·  Dashboard AJAX Controller
   ═══════════════════════════════════════════════════════════════ */

/* ── CSRF ────────────────────────────────────────────────────── */
function getCsrf() {
  for (const raw of document.cookie.split(';')) {
    const c = raw.trim();
    if (c.startsWith('csrftoken=')) return decodeURIComponent(c.slice(10));
  }
  return '';
}

/* ── ERROR DISPLAY ───────────────────────────────────────────── */
function showErr(id, errors) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = Object.entries(errors)
    .map(([k, v]) => (k === '__all__' ? v.join(', ') : k + ': ' + v.join(', ')))
    .join(' | ');
  el.classList.add('visible');
}
function clearErr(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = '';
  el.classList.remove('visible');
}

/* ── FETCH STATS ─────────────────────────────────────────────── */
async function fetchStats() {
  try {
    const r = await fetch('/dashboard/stats/');
    if (!r.ok) return;
    const d = await r.json();
    const set = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
    set('count-participants', d.participants);
    set('count-events', d.events);
    set('count-attended', d.attended);
    set('count-feedback', d.feedback);
    const pb = document.getElementById('participant-count-badge');
    if (pb) pb.textContent = d.participants + ' registered';
  } catch (_) {}
}

/* ── FETCH & REFRESH TABLE ───────────────────────────────────── */
async function fetchRows() {
  try {
    const r = await fetch('/dashboard/participants/');
    if (!r.ok) return;
    const d = await r.json();
    const tb = document.getElementById('participant-table-body');
    if (tb) tb.innerHTML = d.html;
  } catch (_) {}
}

/* ── ADD STUDENT ─────────────────────────────────────────────── */
const participantForm = document.getElementById('participant-form');
if (participantForm) {
  participantForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearErr('participant-errors');
    const btn = participantForm.querySelector('[type=submit]');
    const orig = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Adding…';
    try {
      const r = await fetch('/dashboard/add-user/', {
        method: 'POST',
        body: new FormData(participantForm),
        headers: { 'X-CSRFToken': getCsrf() },
      });
      if (!r.ok) {
        const d = await r.json().catch(() => ({}));
        showErr('participant-errors', d.errors || { error: ['Unable to add student. Check all fields.'] });
        showToast('Fix the form errors', 'error');
      } else {
        participantForm.reset();
        await fetchRows();
        await fetchStats();
        showToast('Student added successfully!');
      }
    } catch (_) {
      showToast('Network error', 'error');
    } finally {
      btn.disabled = false;
      btn.innerHTML = orig;
    }
  });
}

/* ── ADD EVENT ───────────────────────────────────────────────── */
const eventForm = document.getElementById('event-form');
if (eventForm) {
  eventForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearErr('event-errors');
    const btn = eventForm.querySelector('[type=submit]');
    const orig = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Adding…';
    try {
      const r = await fetch('/dashboard/add-event/', {
        method: 'POST',
        body: new FormData(eventForm),
        headers: { 'X-CSRFToken': getCsrf() },
      });
      if (!r.ok) {
        const d = await r.json().catch(() => ({}));
        showErr('event-errors', d.errors || { error: ['Unable to add event.'] });
        showToast('Fix the form errors', 'error');
      } else {
        const d = await r.json();
        eventForm.reset();
        const list = document.getElementById('event-list');
        // Remove empty-state placeholder if present
        const emptyDiv = list.querySelector('.empty-state');
        if (emptyDiv) emptyDiv.closest('tr, div.empty-state, div') && emptyDiv.remove();
        // Prepend new event item
        const div = document.createElement('div');
        div.className = 'event-item';
        div.dataset.eventId = d.event.id;
        div.innerHTML =
          '<div style="display:flex;gap:.6rem;align-items:flex-start;flex:1;min-width:0;">' +
            '<span class="event-dot"></span>' +
            '<div style="min-width:0;">' +
              '<div class="event-name">' + d.event.title + '</div>' +
              '<div class="event-meta">' + d.event.event_date + ' · ' + (d.event.description || 'No description') + '</div>' +
            '</div>' +
          '</div>' +
          '<button class="btn btn-icon btn-red delete-event"' +
          ' data-url="/dashboard/delete-event/' + d.event.id + '/"' +
          ' title="Delete event"><i class="bi bi-trash3-fill"></i></button>';
        list.prepend(div);
        await fetchStats();
        showToast('Event "' + d.event.title + '" created!');
      }
    } catch (_) {
      showToast('Network error', 'error');
    } finally {
      btn.disabled = false;
      btn.innerHTML = orig;
    }
  });
}

/* ── GLOBAL CLICK DELEGATION ─────────────────────────────────── */
document.addEventListener('click', async (e) => {

  /* Attendance toggle */
  const tog = e.target.closest('.attendance-toggle');
  if (tog) {
    tog.disabled = true;
    try {
      const r = await fetch(tog.dataset.url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCsrf(),
        },
      });
      if (r.ok) {
        const d = await r.json();
        await fetchRows();
        await fetchStats();
        showToast(d.attendance ? '✓ Attendance marked' : 'Attendance removed', d.attendance ? 'success' : 'info');
      } else {
        showToast('Could not toggle attendance', 'error');
      }
    } catch (_) { showToast('Network error', 'error'); }
    // button is re-rendered by fetchRows(), no need to re-enable
    return;
  }

  /* Delete student */
  const delS = e.target.closest('.delete-student');
  if (delS) {
    if (!confirm('Remove this participant? This cannot be undone.')) return;
    try {
      const r = await fetch(delS.dataset.url, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrf() },
      });
      if (r.ok) {
        await fetchRows();
        await fetchStats();
        showToast('Participant removed.', 'info');
      } else {
        showToast('Could not delete participant', 'error');
      }
    } catch (_) { showToast('Network error', 'error'); }
    return;
  }

  /* Delete event */
  const delE = e.target.closest('.delete-event');
  if (delE) {
    if (!confirm('Delete this event?')) return;
    try {
      const r = await fetch(delE.dataset.url, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrf() },
      });
      if (r.ok) {
        const item = delE.closest('[data-event-id]');
        if (item) item.remove();
        await fetchStats();
        showToast('Event deleted.', 'info');
      } else {
        showToast('Could not delete event', 'error');
      }
    } catch (_) { showToast('Network error', 'error'); }
    return;
  }
});

/* ── MARKS SAVE ──────────────────────────────────────────────── */
/*
 * KEY FIX: The marks form now includes {% csrf_token %} in the template,
 * so new FormData(form) automatically picks it up — no manual header needed.
 * The view fix (commit=False + instance.save(update_fields=['marks']))
 * means this will now actually persist to the database.
 */
document.addEventListener('submit', async (e) => {
  const form = e.target.closest('.marks-form');
  if (!form) return;
  e.preventDefault();

  const btn = form.querySelector('[type=submit]');
  const orig = btn ? btn.innerHTML : '';
  if (btn) { btn.disabled = true; btn.innerHTML = '<i class="bi bi-hourglass-split"></i>'; }

  const marksVal = form.querySelector('[name=marks]').value;
  if (marksVal === '' || marksVal === null) {
    showToast('Enter a mark between 0 and 100', 'error');
    if (btn) { btn.disabled = false; btn.innerHTML = orig; }
    return;
  }

  try {
    const r = await fetch(form.dataset.url, {
      method: 'POST',
      body: new FormData(form),   // includes csrfmiddlewaretoken from the form
      headers: { 'X-CSRFToken': getCsrf() },  // belt-and-suspenders
    });
    if (!r.ok) {
      const d = await r.json().catch(() => ({}));
      const msg = d.errors ? JSON.stringify(d.errors) : 'Invalid marks value';
      showToast(msg, 'error');
    } else {
      await fetchRows();   // re-render table (updates badge + progress bar)
      await fetchStats();
      showToast('Marks saved ✓');
    }
  } catch (_) {
    showToast('Network error — marks not saved', 'error');
  } finally {
    // btn is re-created by fetchRows, so no need to restore
  }
});

/* ── INIT ────────────────────────────────────────────────────── */
fetchStats();
setInterval(fetchStats, 8000);