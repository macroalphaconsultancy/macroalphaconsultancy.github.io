async function loadResearch(){
  try{
    const res = await fetch('research.json');
    const data = await res.json();
    const grid = document.getElementById('research-grid');
    data.forEach(item => {
      const card = document.createElement('a');
      card.className = 'research-card';
      card.href = item.url;
      card.target = '_blank';
      card.rel = 'noopener';
      card.innerHTML = `
        <div class="research-icon">${getIcon(item.source)}</div>
        <div class="research-content">
          <h4>${escapeHtml(item.title)}</h4>
          <p>${escapeHtml(item.summary)} <span style="opacity:.8">— ${escapeHtml(item.author)}</span></p>
        </div>
      `;
      grid.appendChild(card);
    });
  }catch(e){
    console.error('Failed to load research.json', e);
  }
}
function getIcon(src){
  const s = (src||'').toLowerCase();
  if(s.includes('medium')) return '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2 5.75C2 4.23122 3.23122 3 4.75 3H19.25C20.7688 3 22 4.23122 22 5.75V18.25C22 19.7688 20.7688 21 19.25 21H4.75C3.23122 21 2 19.7688 2 18.25V5.75Z" fill="#F2EECF"/></svg>';
  if(s.includes('substack')) return 'S';
  return '🔗';
}
function escapeHtml(text){ return text? text.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])) : '' }
loadResearch();
