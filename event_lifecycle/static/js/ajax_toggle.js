function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (const raw of cookies) {
      const cookie = raw.trim();
      if (cookie.startsWith(`${name}=`)) {
        cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrfToken = getCookie('csrftoken');

async function fetchStats() {
  const response = await fetch('/dashboard/stats/');
  if (!response.ok) return;
  const data = await response.json();
  document.getElementById('count-participants').textContent = data.participants;
  document.getElementById('count-events').textContent = data.events;
  document.getElementById('count-attended').textContent = data.attended;
  document.getElementById('count-feedback').textContent = data.feedback;
}

async function fetchParticipantRows() {
  const response = await fetch('/dashboard/participants/');
  if (!response.ok) return;
  const data = await response.json();
  document.getElementById('participant-table-body').innerHTML = data.html;
}

function showErrors(targetId, errors) {
  const target = document.getElementById(targetId);
  const list = Object.entries(errors).map(([k, v]) => `${k}: ${v.join(', ')}`);
  target.textContent = list.join(' | ');
}

const participantForm = document.getElementById('participant-form');
if (participantForm) {
  participantForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    document.getElementById('participant-errors').textContent = '';
    const formData = new FormData(participantForm);
    const response = await fetch('/dashboard/add-user/', {
      method: 'POST',
      body: formData,
      headers: { 'X-CSRFToken': csrfToken },
    });

    if (!response.ok) {
      const data = await response.json();
      showErrors('participant-errors', data.errors || { error: ['Unable to add user.'] });
      return;
    }

    participantForm.reset();
    await fetchParticipantRows();
    await fetchStats();
  });
}

const eventForm = document.getElementById('event-form');
if (eventForm) {
  eventForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    document.getElementById('event-errors').textContent = '';
    const formData = new FormData(eventForm);
    const response = await fetch('/dashboard/add-event/', {
      method: 'POST',
      body: formData,
      headers: { 'X-CSRFToken': csrfToken },
    });

    if (!response.ok) {
      const data = await response.json();
      showErrors('event-errors', data.errors || { error: ['Unable to add event.'] });
      return;
    }

    const data = await response.json();
    eventForm.reset();
    const li = document.createElement('li');
    li.className = 'list-group-item px-0';
    li.innerHTML = `<strong>${data.event.title}</strong><br><small class="text-muted">${data.event.event_date} — ${data.event.description}</small>`;
    document.getElementById('event-list').prepend(li);
    await fetchStats();
  });
}

document.addEventListener('click', async (event) => {
  const button = event.target.closest('.attendance-toggle');
  if (!button) return;

  const response = await fetch(button.dataset.url, {
    method: 'POST',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrfToken,
    },
  });

  if (!response.ok) return;
  await fetchParticipantRows();
  await fetchStats();
});

fetchStats();
setInterval(fetchStats, 5000);
