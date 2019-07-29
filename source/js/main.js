import "babel-polyfill";

import Tabs from "./components/tabs";
import MenuToggle from "./components/menu-toggle";
import AmountToggle from "./components/donation-amount-toggle";
import CurrencySelect from "./components/currency-selector.js";

// Manage tab index for primary nav
function tabIndexer() {
  document.querySelectorAll("[data-nav-tab-index]").forEach(navLink => {
    navLink.tabIndex = "-1";
  });
}

// Open the mobile menu callback
function openMenu() {
  document.querySelector("[data-primary-nav]").classList.add("is-visible");
  document.querySelectorAll("[data-nav-tab-index]").forEach(navLink => {
    navLink.removeAttribute("tabindex");
  });
}

// Close the mobile menu callback
function closeMenu() {
  document.querySelector("[data-primary-nav]").classList.remove("is-visible");
  tabIndexer();
}

document.addEventListener("DOMContentLoaded", function() {
  for (const menutoggle of document.querySelectorAll(MenuToggle.selector())) {
    new MenuToggle(menutoggle, openMenu, closeMenu);
  }

  for (const donatetoggle of document.querySelectorAll(
    AmountToggle.selector()
  )) {
    new AmountToggle(donatetoggle);
  }

  for (const tabs of document.querySelectorAll(Tabs.selector())) {
    new Tabs(tabs);
  }

  tabIndexer();

  for (const currencySelect of document.querySelectorAll(
    CurrencySelect.selector()
  )) {
    new CurrencySelect(currencySelect);
  }
});
