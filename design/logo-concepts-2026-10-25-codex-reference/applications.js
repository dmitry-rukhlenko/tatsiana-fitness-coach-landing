const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));

function selectTab(tab, updateAddress = true) {
  const selected = tabs.indexOf(tab);
  if (selected < 0) return;

  tabs.forEach((item, index) => {
    const active = index === selected;
    item.setAttribute('aria-selected', String(active));
    item.tabIndex = active ? 0 : -1;
    panels[index].hidden = !active;
  });

  // Replace the hash without jumping down the page or adding history entries.
  if (updateAddress) history.replaceState(null, '', tab.getAttribute('href'));
}

tabs.forEach((tab, index) => {
  tab.addEventListener('pointerenter', event => {
    if (event.pointerType === 'mouse' || event.pointerType === 'pen') selectTab(tab);
  });
  tab.addEventListener('focus', () => selectTab(tab));
  tab.addEventListener('click', event => {
    event.preventDefault();
    selectTab(tab);
  });
  tab.addEventListener('keydown', event => {
    let next;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = tabs.length - 1;
    if (next === undefined) return;
    event.preventDefault();
    tabs[next].focus({ preventScroll: true });
  });
});

function selectFromAddress() {
  selectTab(tabs.find(tab => tab.getAttribute('href') === location.hash) || tabs[0], false);
}

window.addEventListener('hashchange', selectFromAddress);
selectFromAddress();
