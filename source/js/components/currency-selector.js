class CurrencySelect {
  static selector() {
    return "#id_currency-switcher-currency";
  }

  constructor(node) {
    this.selectMenu = node;
    this.formContainer = document.getElementById("js-donate-form");
    this.data = JSON.parse(document.getElementById("currencies").innerHTML);
    this.oneOffContainer = document.getElementById("js-donate-form-single");
    this.monthlyContainer = document.getElementById("js-donate-form-monthly");
    this.defaultCurrency = document.getElementById(
      "id_currency-switcher-currency"
    ).value;

    this.bindEvents();
  }

  // Get correct currency data from json based on select choice
  getSelectValue() {
    var value = this.selectMenu[this.selectMenu.selectedIndex].value;
    var selectedData = this.data[value];

    this.assignValues(selectedData);
  }

  assignValues(selectedData) {
    // Create arrays for monthly and one off based on data
    var oneOffValues = selectedData.presets.single;
    var monthlyValue = selectedData.presets.monthly;
    var currency = selectedData.symbol;

    // Check if papal is needed
    this.checkPaypal(selectedData);

    // Create buttons
    this.outputOptions(
      oneOffValues,
      "one-time-amount",
      currency,
      this.oneOffContainer
    );
    this.outputOptions(
      monthlyValue,
      "monthly-amount",
      currency,
      this.monthlyContainer
    );

    this.updateCurrency(currency);
  }

  // Output donation form buttons
  outputOptions(data, type, currency, container) {
    var container = container;

    container.innerHTML = data
      .map((donationValue, index) => {
        return `<div class='donation-amount'>
                    <input type='radio' class='donation-amount__radio' name='amount' value='${donationValue}' id='${type}-${index}' autocomplete='off'>
                    <label for='${type}-${index}' class='donation-amount__label'>
                        ${currency}${donationValue} ${
          type === "monthly-amount" ? "per month" : ""
        }
                    </label>
                </div>`;
      })
      .join("");

    container.insertAdjacentHTML(
      "beforeend",
      `<div class='donation-amount donation-amount--two-col donation-amount--other'><input type='radio' class='donation-amount__radio' name='amount' value='other' id='${type}-other' autocomplete='off' data-other-amount-radio><label for='${type}-other' class='donation-amount__label' data-currency>$</label><input type='text' class='donation-amount__input' id='${type}-other-input' placeholder='Other amount' data-other-amount></div>`
    );
  }

  updateCurrency(currency) {
    // Update currency symbol
    document.querySelectorAll("[data-currency]").forEach(currencyitem => {
      currencyitem.innerHTML = currency;
    });

    // Other amount vars
    this.otherAmountInput = document.querySelectorAll("[data-other-amount]");
    this.otherAmountLabel = document.querySelectorAll("[data-currency]");
    this.otherAmountRadio = document.querySelectorAll(
      "[data-other-amount-radio]"
    );

    this.bindOtherAmountEvents();
  }

  // Add class to container if paypal should be disabled
  checkPaypal(selectedData) {
    if (selectedData.disabled == "paypal") {
      this.formContainer.classList.add("paypal-disabled");
    } else {
      this.formContainer.classList.remove("paypal-disabled");
    }
  }

  // Update Radio to checked
  selectRadio(event) {
    this.otherAmountRadio.forEach(radio => {
      radio.checked = true;
    });
  }

  // Updated radio value based on custom input
  updateValue(event) {
    const value = parseFloat(event.target.value).toFixed(2);
    this.otherAmountRadio.forEach(radiovalue => {
      radiovalue.value = value;
    });
  }

  bindEvents() {
    if (!this.selectMenu) {
      return;
    }

    // On select choice
    this.selectMenu.addEventListener("change", () => {
      this.getSelectValue();
    });
  }

  bindOtherAmountEvents() {
    for (var i = 0; i < this.otherAmountInput.length; i++) {
      this.otherAmountInput[i].addEventListener("click", event =>
        this.selectRadio(event)
      );
      this.otherAmountInput[i].addEventListener("change", event =>
        this.updateValue(event)
      );
    }
  }
}

export default CurrencySelect;
