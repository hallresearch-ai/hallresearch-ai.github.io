'use strict';
document.documentElement.classList.add('js');
const button = document.querySelector('.mobile-toggle');
const rail = document.querySelector('.catalog-rail');
const mobile = window.matchMedia('(max-width: 1050px)');
function closeMenu(restoreFocus = false) {
  rail?.classList.remove('open');
  button?.setAttribute('aria-expanded', 'false');
  if (restoreFocus) button?.focus();
}
if (button && rail) {
  button.hidden = false;
  button.addEventListener('click', () => {
    const expanded = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(expanded));
    rail.classList.toggle('open', expanded);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && rail.classList.contains('open')) closeMenu(true);
  });
  document.addEventListener('click', (event) => {
    if (!rail.contains(event.target) && !button.contains(event.target)) closeMenu();
  });
  mobile.addEventListener('change', () => closeMenu());
}
const compact = window.matchMedia('(max-width: 850px)');
function updateSectionNavigation() {
  document.querySelectorAll('.sidebar details').forEach((detail) => { detail.open = !compact.matches; });
}
updateSectionNavigation();
compact.addEventListener('change', updateSectionNavigation);
