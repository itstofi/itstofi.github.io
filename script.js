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
    alt: 'PrivateRAG AI Chat screen with workspace and local model selectors',
    label: 'Show document view',
  },
  documents: {
    src: 'assets/private-rag-documents.png',
    alt: 'PrivateRAG AI document management screen with locally indexed sample files',
    label: 'Show chat view',
  },
};

toggle?.addEventListener('click', () => {
  const showingDocuments = toggle.dataset.view === 'documents';
  const nextView = showingDocuments ? 'chat' : 'documents';
  const next = views[nextView];
  projectImage.src = next.src;
  projectImage.alt = next.alt;
  toggle.textContent = next.label;
  toggle.dataset.view = nextView;
});
