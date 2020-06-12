class AmountToggle {
  static selector() {
    return "[data-amount-toggle]";
  }

  constructor(node) {
    this.toggleButton = node;
    this.updateButton = document.querySelector("#js-update-button");
    this.actionsContainer = document.querySelector("[data-amount-actions]");
    this.hiddenInput = document.querySelector("#id_amount");
    this.updateForm = document.querySelector("#js-update-donation-amount-form");
    this.inputForm = document.querySelector("#js-update-donation-value");
    this.activeClass = "active";
    this.selectedClass = "selected";

    let locale = this.updateForm.getAttribute("data-locale").replace("_", "-");
    let currency = this.updateForm.getAttribute("data-currency").toUpperCase();
    this.formatter = new Intl.NumberFormat(locale, {
      style: "currency",
      currency: currency,
      minimumFractionDigits: 0,
    });

    this.bindEvents();
  }

  UpdateHiddenInputFromInput(event) {
    if (this.inputForm.reportValidity()) {
      // Convert the number to 2 decimal places if needed
      this.inputForm.value = parseFloat(this.inputForm.value).toFixed(2);
      this.hiddenInput.value = this.inputForm.value;
      // Hide form after updating hidden input
      this.toggleOptions(event);
      // Change values that exist on the page
      this.UpdatePageDonationAmount();
    }
  }

  UpdatePageDonationAmount() {
    document
      .querySelectorAll(".js-donation-value")
      .forEach((donationAmount) => {
        donationAmount.textContent = this.formatter.format(
          this.hiddenInput.value
        );
      });
  }

  toggleOptions(event) {
    event.preventDefault();
    this.toggleButton.classList.toggle(this.selectedClass);
    this.actionsContainer.classList.toggle(this.activeClass);
  }

  validateForm(event) {
    const value = this.inputForm.value;

    if (!value) {
      this.inputForm.dataset.state = "invalid";
      this.inputForm.classList.add("form-item__standalone-error");
      this.updateButton.setAttribute("disabled", "disabled");
      return;
    }

    const trimmed = value.trim();

    if (trimmed) {
      this.inputForm.dataset.state = "valid";
      this.updateButton.removeAttribute("disabled");
      this.inputForm.classList.remove("form-item__standalone-error");
    }
  }

  bindEvents() {
    if (!this.toggleButton) {
      return;
    }

    this.toggleButton.addEventListener("click", (event) =>
      this.toggleOptions(event)
    );

    this.updateButton.addEventListener("click", (event) =>
      this.UpdateHiddenInputFromInput(event)
    );

    this.updateForm.addEventListener("input", (evt) => {
      this.validateForm(event);
    });

    // Don't submit the form
    this.updateForm.addEventListener("submit", (event) =>
      event.preventDefault()
    );
  }
}

export default AmountToggle;
