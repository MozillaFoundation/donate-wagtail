import 'babel-polyfill';

import MenuToggle from './components/menu-toggle';

// Open the mobile menu callback
function openMenu() {
    document.querySelector('[data-primary-nav]').classList.add('is-visible');
}

// Close the mobile menu callback.
function closeMenu() {
    document.querySelector('[data-primary-nav]').classList.remove('is-visible');
}

document.addEventListener('DOMContentLoaded', function() {

    for (const menutoggle of document.querySelectorAll(MenuToggle.selector())) {
        new MenuToggle(menutoggle, openMenu, closeMenu);
    }

});
