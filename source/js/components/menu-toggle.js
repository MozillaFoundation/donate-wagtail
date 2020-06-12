class MenuToggle {
  static selector() {
    return "[data-menu-toggle]";
  }

  constructor(node, openCb = () => {}, closeCb = () => {}) {
    this.node = node;

    // Any callbacks to be called on open or close.
    this.openCb = openCb;
    this.closeCb = closeCb;

    this.state = {
      open: false,
    };

    this.bindEventListeners();
  }

  bindEventListeners() {
    this.node.addEventListener("click", () => {
      this.toggle();
    });
  }

  toggle() {
    this.state.open ? this.close() : this.open();
  }

  open() {
    this.node.classList.add("is-open");
    this.openCb();

    this.state.open = true;
  }

  close() {
    this.node.classList.remove("is-open");
    this.closeCb();

    this.state.open = false;
  }
}

export default MenuToggle;
