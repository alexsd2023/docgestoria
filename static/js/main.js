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

function solicitarDocumento(clienteId, btn) {
  const tipo = btn.dataset.tipo;
  fetch(`/clientes/${clienteId}/documentos/solicitar`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tipo }),
  })
  .then(r => r.json())
  .then(data => {
    if (data.email_enviado) {
      showToast('Solicitado y email enviado al cliente ✓');
    } else {
      showToast('Documento solicitado, pero el email falló: ' + (data.email_error || 'error desconocido'));
    }
    setTimeout(() => location.reload(), 1400);
  });
}

function subirArchivoChecklist(clienteId, inputEl) {
  const archivo = inputEl.files[0];
  if (!archivo) return;
  const tipo = inputEl.dataset.tipo;
  const form = new FormData();
  form.append('archivo', archivo);
  form.append('tipo', tipo);
  showToast('Subiendo archivo...');
  fetch(`/clientes/${clienteId}/documentos/subir`, { method: 'POST', body: form })
    .then(r => r.json())
    .then(data => {
      if (data.ok) {
        showToast('Archivo subido ✓');
        setTimeout(() => location.reload(), 900);
      } else {
        showToast(data.error || 'Error al subir el archivo');
      }
    });
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});

// ---- Buscador de la topbar ----
(function () {
  const input = document.getElementById('topbar-search');
  const dropdown = document.getElementById('search-dropdown');
  if (!input || !dropdown) return;

  let temporizador = null;

  function escapeHtml(str) {
    return String(str ?? '').replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[c]));
  }

  function buscarEnVivo(q) {
    fetch(`/api/buscar?q=${encodeURIComponent(q)}`)
      .then(r => r.json())
      .then(data => {
        const resultados = data.resultados || [];
        if (resultados.length === 0) {
          dropdown.innerHTML = '<div class="search-empty">Sin resultados</div>';
        } else {
          dropdown.innerHTML = resultados.map(c => `
            <div class="search-result-item" onclick="window.location='/clientes/${c.id}'">
              <div class="avatar ${escapeHtml(c.color)}" style="width:26px;height:26px;font-size:10px">${escapeHtml(c.initials)}</div>
              <div style="min-width:0">
                <div style="font-size:13px;font-weight:500;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${escapeHtml(c.nombre)}</div>
                <div style="font-size:11px;color:var(--text-3);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${escapeHtml(c.tramite)}</div>
              </div>
            </div>
          `).join('');
        }
        dropdown.classList.add('show');
      });
  }

  input.addEventListener('input', () => {
    clearTimeout(temporizador);
    const q = input.value.trim();
    if (q.length < 2) {
      dropdown.classList.remove('show');
      dropdown.innerHTML = '';
      return;
    }
    temporizador = setTimeout(() => buscarEnVivo(q), 250);
  });

  input.addEventListener('focus', () => {
    if (input.value.trim().length >= 2 && dropdown.innerHTML) dropdown.classList.add('show');
  });

  document.addEventListener('click', e => {
    if (!e.target.closest('.search-wrap')) dropdown.classList.remove('show');
  });
})();
