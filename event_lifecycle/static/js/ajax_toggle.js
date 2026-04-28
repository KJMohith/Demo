function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i += 1) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(`${name}=`)) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrfToken = getCookie('csrftoken');

for (const button of document.querySelectorAll('.attendance-toggle')) {
  button.addEventListener('click', async () => {
    const response = await fetch(button.dataset.url, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrfToken,
      },
    });

    if (!response.ok) {
      return;
    }

    const data = await response.json();
    button.textContent = data.attendance ? '✅' : '❌';
  });
}
