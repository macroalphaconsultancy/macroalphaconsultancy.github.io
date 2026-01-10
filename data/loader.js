// Universal Data Loader for Macro Dashboards

async function loadMacroData() {
  const [rawRes, derivedRes] = await Promise.all([
    fetch('/data/raw.json'),
    fetch('/data/derived.json')
  ]);

  const raw = await rawRes.json();
  const derived = await derivedRes.json();

  document.querySelectorAll('[data-key]').forEach(el => {
    const key = el.getAttribute('data-key');
    let value = null;

    if (raw[key] && raw[key].value !== null) {
      value = raw[key].value;
    } else if (derived[key] !== undefined && derived[key] !== null) {
      value = derived[key];
    }

    if (value !== null) {
      el.textContent = typeof value === 'number'
        ? value.toFixed(2)
        : value;
    }
  });
}

document.addEventListener('DOMContentLoaded', loadMacroData);
