function openModal() { document.getElementById('modal').classList.add('open'); }
function closeModal() { document.getElementById('modal').classList.remove('open'); }

function showToast(msg) {
  const t = document.getElementById('toast');
  document.getElementById('toast-msg').textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2800);
}

function submitNuevoCliente() {
  const body = {
    nombre: document.getElementById('f-nombre').value,
    apellidos: document.getElementById('f-apellidos').value,
    email: document.getElementById('f-email').value,
    tel: document.getElementById('f-tel').value,
    dni: document.getElementById('f-dni').value,
    tramite: document.getElementById('f-tramite').value,
  };
  fetch('/clientes/nuevo', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  .then(r => r.json())
  .then(data => {
    closeModal();
    showToast('Cliente ' + data.nombre + ' creado');
    setTimeout(() => location.reload(), 1000);
  });
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});
