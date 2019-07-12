import 'babel-polyfill';

import Tabs from './components/tabs';
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

    for (const tabs of document.querySelectorAll(Tabs.selector())) {
        new Tabs(tabs);
    }

});
