import gaEvent from "./analytics";

class Tabs {
  static selector() {
    return ".js-tab-item";
  }

  constructor(node) {
    this.tab = node;
    this.tabset = this.tab.closest(".js-tabs");
    this.allTabs = this.tabset.querySelectorAll(".js-tab-item");
    let tabPanelId = this.tab.getAttribute("aria-controls");
    this.tabPanel = document.getElementById(tabPanelId);
    this.allTabPanels = this.tabset.querySelectorAll(".js-tab-panel");
    this.bindEvents();
  }

  bindEvents() {
    this.tab.addEventListener("click", e => {
      for (let tab of this.allTabs) {
        tab.classList.remove("active");
        tab.setAttribute("aria-selected", "false");
      }

      for (let tabPanel of this.allTabPanels) {
        tabPanel.classList.add("tabs__panel--hidden");
      }

      this.tab.classList.add("active");
      this.tab.setAttribute("aria-selected", "true");
      this.tabPanel.classList.remove("tabs__panel--hidden");
      gaEvent({
        eventCategory: "User Flow",
        eventAction: "Changed Frequency",
        eventLabel: this.tab.getAttribute("data-label")
      });
    });
  }
}

export default Tabs;
