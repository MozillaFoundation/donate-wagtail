import 'babel-polyfill';

import MobileMenu from './components/mobile-menu';
import MobileSubMenu from './components/mobile-sub-menu';

// Open the mobile menu callback
function openMobileMenu() {
    document.querySelector('body').classList.add('no-scroll');
    document.querySelector('[data-mobile-menu]').classList.add('is-visible');
}

// Close the mobile menu callback.
function closeMobileMenu() {
    document.querySelector('body').classList.remove('no-scroll');
    document.querySelector('[data-mobile-menu]').classList.remove('is-visible');
}

document.addEventListener('DOMContentLoaded', function() {

    for (const mobilemenu of document.querySelectorAll(MobileMenu.selector())) {
        new MobileMenu(mobilemenu, openMobileMenu, closeMobileMenu);
    }

    for (const mobilesubmenu of document.querySelectorAll(MobileSubMenu.selector())) {
        new MobileSubMenu(mobilesubmenu);
    }

    // Toggle subnav visibility
    for (const subnavBack of document.querySelectorAll('[data-subnav-back]')) {
        subnavBack.addEventListener('click', () => {
            subnavBack.parentNode.classList.remove('is-visible');
        });
    }

});
