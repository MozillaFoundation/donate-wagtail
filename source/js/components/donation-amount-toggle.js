class AmountToggle {
  static selector() {
    return "[data-amount-toggle]";
  }

  constructor(node) {
    this.toggleButton = node;
    this.updateButton = document.querySelector("#js-update-button");
    this.actionsContainer = document.querySelector("[data-amount-actions]");
    this.hiddenInput = document.querySelector("#id_amount");
    this.activeClass = "active";
    this.selectedClass = "selected";

    this.bindEvents();
  }

  UpdateHiddenInputFromInput(event) {
    event.preventDefault();
    let input = document.querySelector("#js-update-donation-value");
    this.hiddenInput.value = input.value;
    // Hide form after updating hidden input
    this.toggleOptions(event);
    // Change values that exist on the page
    this.UpdatePageDonationAmount();
  }

  UpdatePageDonationAmount() {
    document.querySelectorAll(".js-donation-value").forEach(donationAmount => {
      donationAmount.textContent = this.hiddenInput.value;
    });
  }

  toggleOptions(event) {
    event.preventDefault();
    this.toggleButton.classList.toggle(this.selectedClass);
    this.actionsContainer.classList.toggle(this.activeClass);
  }

  bindEvents() {
    if (!this.toggleButton) {
      return;
    }

    this.toggleButton.addEventListener("click", event =>
      this.toggleOptions(event)
    );

    this.updateButton.addEventListener("click", event =>
      this.UpdateHiddenInputFromInput()
    );
  }
}

export default AmountToggle;
