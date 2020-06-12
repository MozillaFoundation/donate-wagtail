class Accordion {
  static selector() {
    return "[data-accordion]";
  }

  constructor(node) {
    this.accordion = node;
    this.question = this.accordion.querySelector("[data-accordion-question]");
    this.answer = this.accordion.querySelector("[data-accordion-answer]");
    this.bindEvents();
  }

  bindEvents() {
    this.question.addEventListener("click", (e) => {
      e.preventDefault();
      let open = this.accordion.classList.contains("is-open");
      this.accordion.classList.toggle("is-open");

      if (open) {
        this.question.setAttribute("aria-expanded", "false");
        this.question.setAttribute("tab-index", 0);
        this.answer.setAttribute("aria-hidden", "true");
        open = false;
      } else {
        this.question.setAttribute("aria-expanded", "true");
        this.question.setAttribute("tab-index", -1);
        this.answer.setAttribute("aria-hidden", "false");
        open = true;
      }
    });

    this.question.addEventListener("focus", () => {
      this.question.setAttribute("aria-selected", "true");
    });

    this.question.addEventListener("blur", () => {
      this.question.setAttribute("aria-selected", "false");
    });
  }
}

export default Accordion;
