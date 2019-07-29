class CurrencySelect {
  static selector() {
    return "#id_currency";
  }

  constructor(node) {
    this.selectMenu = node;
    this.formContainer = document.getElementById("js-donate-form");
    this.data = JSON.parse(document.getElementById("currencies").innerHTML);

    // this.selectValue = this.selectMenu[this.selectMenu.selectedIndex].value;
    this.oneOffContainer = document.getElementById("js-donate-form-single");
    this.monthlyContainer = document.getElementById("js-donate-form-monthly");

    this.bindEvents();
  }

  // Get correct currency data from json
  getSelectValue() {
    var value = this.selectMenu[this.selectMenu.selectedIndex].value;
    var selectedData = this.data[value];

    // Create arrays for monthly and one off based on data
    var oneOffValues = selectedData.presets.single;
    var monthlyValue = selectedData.presets.monthly;
    var currency = selectedData.symbol;

    // Update currency symbol
    document.querySelectorAll("[data-currency]").forEach(currencyitem => {
      currencyitem.innerHTML = currency;
    });

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
  }

  // Output donation form buttons
  outputOptions(data, type, currency, container) {
    var container = container;

    container.innerHTML = data
      .map((donationValue, index) => {
        return `<div class='donation-amount'>
                    <input type='radio' class='donation-amount__radio' name='amount' value='${donationValue}' id='${type}-${index}' autocomplete='off'>
                    <label for='${type}-${index}' class='donation-amount__label'>${currency}${donationValue}</label>
                </div>`;
      })
      .join("");
  }

  // Add class to container if paypal should be disabled
  checkPaypal(selectedData) {
    if (selectedData.disabled == "paypal") {
      this.formContainer.classList.add("paypal-disabled");
    } else {
      this.formContainer.classList.remove("paypal-disabled");
    }
  }

  bindEvents() {
    if (!this.selectMenu) {
      return;
    }

    this.selectMenu.addEventListener("change", () => {
      this.getSelectValue();
    });
  }
}

export default CurrencySelect;
