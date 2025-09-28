const API_BASE = 'http://127.0.0.1:8000';

async function fetchRuns() {
  const res = await fetch(`${API_BASE}/runs`);
  const runs = await res.json();
  const body = document.getElementById('runsBody');
  body.innerHTML = '';
  runs.forEach(r => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${r.id}</td>
      <td>${r.name}</td>
      <td>${r.status}</td>
      <td>${r.total_tests}</td>
      <td>${r.passed}</td>
      <td>${r.failed}</td>
      <td>${new Date(r.created_at).toLocaleString()}</td>
      <td><button data-id="${r.id}" class="view-btn">View</button></td>
    `;
    body.appendChild(tr);
  });

  document.querySelectorAll('.view-btn').forEach(btn => {
    btn.addEventListener('click', () => showRunDetails(btn.getAttribute('data-id')));
  });
}

async function showRunDetails(runId) {
  const res = await fetch(`${API_BASE}/runs/${runId}`);
  if (!res.ok) {
    document.getElementById('runMeta').textContent = `Run ${runId} not found.`;
    document.getElementById('testsBody').innerHTML = '';
    return;
  }
  const run = await res.json();
  document.getElementById('runMeta').textContent =
    `Run #${run.id} — ${run.name} — ${run.passed}/${run.total_tests} passed — status: ${run.status}`;

  const tbody = document.getElementById('testsBody');
  tbody.innerHTML = '';
  (run.tests || []).forEach(t => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${escapeHtml(t.name)}</td>
      <td>${t.status}</td>
      <td>${t.duration_ms}</td>
      <td>${escapeHtml(t.message || '')}</td>
    `;
    tbody.appendChild(tr);
  });

  const runIdInput = document.getElementById('runId');
  if (runIdInput) runIdInput.value = run.id;
}

document.getElementById('createRunForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('name').value;
  const branch = document.getElementById('branch').value;
  const commit = document.getElementById('commit').value;
  const res = await fetch(`${API_BASE}/runs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, branch, commit_sha: commit })
  });
  const created = await res.json();
  await fetchRuns();
  showRunDetails(created.id);
  e.target.reset();
});

document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const runId = document.getElementById('runId').value;
  const file = document.getElementById('logFile').files[0];
  const fd = new FormData();
  fd.append('file', file);
  const res = await fetch(`${API_BASE}/runs/${runId}/logs`, { method: 'POST', body: fd });
  if (res.ok) {
    const run = await res.json();
    await fetchRuns();
    document.getElementById('runMeta').textContent =
      `Run #${run.id} — ${run.name} — ${run.passed}/${run.total_tests} passed — status: ${run.status}`;
    const tbody = document.getElementById('testsBody');
    tbody.innerHTML = '';
    (run.tests || []).forEach(t => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${escapeHtml(t.name)}</td>
        <td>${t.status}</td>
        <td>${t.duration_ms}</td>
        <td>${escapeHtml(t.message || '')}</td>
      `;
      tbody.appendChild(tr);
    });
    e.target.reset();
  }
});

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

fetchRuns();
