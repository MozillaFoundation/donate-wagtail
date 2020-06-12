class CopyURL {
  static selector() {
    return "[data-copy-link]";
  }

  constructor(node) {
    this.button = node;
    this.input = this.button.querySelector("[data-copy-value]");
    this.bindEvents();
  }

  copyText() {
    this.input.select();
    this.input.setSelectionRange(0, 99999); /*For mobile devices*/
    document.execCommand("copy");
  }

  updateButton() {
    this.button.classList.add("copied");
  }

  bindEvents() {
    this.button.addEventListener("click", (e) => {
      e.preventDefault();
      this.copyText();
      this.updateButton();
    });
  }
}

export default CopyURL;
