const header = document.querySelector('[data-header]');
const toggle = document.querySelector('[data-visual-toggle]');
const projectImage = document.querySelector('.project-visual img');

const updateHeader = () => {
  header?.classList.toggle('is-scrolled', window.scrollY > 12);
};

window.addEventListener('scroll', updateHeader, { passive: true });
updateHeader();

const views = {
  chat: {
    src: 'assets/private-rag-workspaces.png',
    alt: 'PrivateRAG AI workspace interface showing local status and indexed documents',
    label: 'Show document view',
  },
  documents: {
    src: 'assets/private-rag-documents.png',
    alt: 'PrivateRAG AI document management interface showing five locally indexed sample files',
    label: 'Show chat view',
  },
};

toggle?.addEventListener('click', () => {
  const showingDocuments = toggle.getAttribute('aria-pressed') === 'true';
  const next = showingDocuments ? views.chat : views.documents;
  projectImage.src = next.src;
  projectImage.alt = next.alt;
  toggle.textContent = next.label;
  toggle.setAttribute('aria-pressed', String(!showingDocuments));
});
