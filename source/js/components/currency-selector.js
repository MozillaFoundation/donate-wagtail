import gaEvent from "./analytics";

class CurrencySelect {
  static selector() {
    return "#id_currency-switcher-currency";
  }

  constructor(node) {
    this.selectMenu = node;
    this.formContainer = document.getElementById("js-donate-form");
    // Convert a locale provided by Django in the form en_US to a
    // BCP 47 compliant tag in the form en-US.
    // See https://tools.ietf.org/html/bcp47
    this.locale = this.formContainer
      .getAttribute("data-locale")
      .replace("_", "-");
    this.data = JSON.parse(document.getElementById("currencies").innerHTML);
    this.oneOffContainer = document.getElementById("js-donate-form-single");
    this.monthlyContainer = document.getElementById("js-donate-form-monthly");
    this.defaultCurrency = document.getElementById(
      "id_currency-switcher-currency"
    ).value;

    this.bindEvents();
  }

  // Assign default options
  processSelectDefaultValue() {
    var selectedData = this.data[this.defaultCurrency];
    // Check if payment options are needed
    this.checkDisabled(selectedData);
    // Enable other amount
    this.bindOtherAmountEvents();
    this.bindAnalyticsEvents();
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
    var minAmount = selectedData.minAmount;
    var formatter = new Intl.NumberFormat(this.locale, {
      style: "currency",
      currency: selectedData.code.toUpperCase(),
      minimumFractionDigits: 0,
    });

    // Create buttons
    this.outputOptions(
      oneOffValues,
      minAmount,
      "one-time-amount",
      formatter,
      this.oneOffContainer
    );
    this.outputOptions(
      monthlyValue,
      minAmount,
      "monthly-amount",
      formatter,
      this.monthlyContainer
    );

    // Check if payment options are needed
    this.checkDisabled(selectedData);

    this.updateCurrency(selectedData, formatter);
  }

  // Output donation form buttons
  outputOptions(data, minAmount, type, formatter, container) {
    var container = container;

    container.innerHTML = data
      .map((donationValue, index) => {
        var formattedValue = formatter.format(donationValue);
        return `<div class='donation-amount'>
                    <input type='radio' class='donation-amount__radio' name='amount' value='${donationValue}' id='${type}-${index}' autocomplete='off' ${
          index == 0 ? "checked" : ""
        }>
                    <label for='${type}-${index}' class='donation-amount__label'>
                        ${formattedValue} <span>${
          type === "monthly-amount" ? window.gettext("per month") : ""
        }</span>
                    </label>
                </div>`;
      })
      .join("");

    var otherAmountString = window.gettext("Other amount");
    container.insertAdjacentHTML(
      "beforeend",
      `<div class='donation-amount donation-amount--two-col donation-amount--other'><input type='radio' class='donation-amount__radio' name='amount' value='other' id='${type}-other' autocomplete='off' data-other-amount-radio><label for='${type}-other' class='donation-amount__label' data-currency>$</label><input type='number' class='donation-amount__input' id='${type}-other-input' placeholder='${otherAmountString}' data-other-amount min="${minAmount}" max="10000000"></div>`
    );
  }

  updateCurrency(selectedData, formatter) {
    var formattedParts = formatter.formatToParts(1);
    // Default symbol
    var symbol = selectedData.symbol;
    // ... which we attempt to replace with a localised one
    formattedParts.forEach((part) => {
      if (part["type"] === "currency") {
        symbol = part["value"];
      }
    });

    // Update currency symbol
    document.querySelectorAll("[data-currency]").forEach((currencyitem) => {
      currencyitem.innerHTML = symbol;
    });

    // Update hidden currency inputs
    this.formContainer
      .querySelectorAll(".js-form-currency")
      .forEach((input) => {
        input.value = selectedData.code;
      });

    gaEvent({
      eventCategory: "User Flow",
      eventAction: "Changed Currency",
      eventLabel:
        selectedData.code[0].toUpperCase() + selectedData.code.slice(1), // GA expects format Usd, Gbp
    });

    this.bindOtherAmountEvents();
    this.bindAnalyticsEvents();
  }

  // Add class to container if payment provider should be disabled
  addClassToContainer(items) {
    items.forEach((item) => {
      this.formContainer.classList.add(`${item}-disabled`);
    });
  }

  checkDisabled(selectedData) {
    // Remove existing classes
    Array.from(this.formContainer.classList).forEach((className) => {
      if (className.endsWith("-disabled")) {
        this.formContainer.classList.remove(className);
      }
    });

    // Add Classes to hide payment option
    if (selectedData.disabled) {
      this.addClassToContainer(selectedData.disabled);
    }
  }

  // Updated radio value based on custom input
  updateValue(input) {
    var radio = input.parentNode.querySelector("[data-other-amount-radio]");
    if (input.reportValidity()) {
      radio.value = parseFloat(event.target.value).toFixed(2);
    } else {
      // If the value is not acceptable, set the radio's value to 0
      // so that Paypal payments will fail if the user attempts to start one. We have no way to
      // stop the paypal modal loading once that button is clicked.
      // See https://github.com/paypal/paypal-checkout-components/issues/139
      radio.value = "0";
    }
  }

  bindEvents() {
    if (!this.selectMenu) {
      return;
    }

    // On select choice
    this.selectMenu.addEventListener("change", () => {
      this.getSelectValue();
    });

    // Initial defaults
    this.processSelectDefaultValue();
  }

  bindOtherAmountEvents() {
    const otherAmountInputs = document.querySelectorAll("[data-other-amount]");
    otherAmountInputs.forEach((input) => {
      input.addEventListener("change", (_) => this.updateValue(input));
      input.addEventListener("focusin", (_) => this.updateValue(input));

      const radio = input.parentNode.querySelector("[data-other-amount-radio]");
      input.addEventListener("click", (_) => (radio.checked = true));
      radio.addEventListener("change", (_) =>
        radio.checked ? this.updateValue(input) : false
      );
    });

    // Because we are using minimum amount validation on the other amount,
    // we need to make sure that this amount is emptied if the user
    // selects a preset amount. Otherwise the browser will fail to validate the form.
    const presets = document.querySelectorAll(
      ".donation-amount__radio:not([data-other-amount-radio])"
    );

    const customAmounts = document.querySelectorAll(
      "[data-other-amount-radio]"
    );

    presets.forEach((input) => {
      input.addEventListener("change", (_) => {
        if (input.checked) {
          otherAmountInputs.forEach((other) => (other.value = ""));
          customAmounts.forEach((other) => (other.value = ""));
        }
      });
    });
  }

  bindAnalyticsEvents() {
    for (const input of this.formContainer.querySelectorAll(
      ".donation-amount__radio"
    )) {
      input.addEventListener("input", (e) => {
        if (
          e.target.checked &&
          !e.target.hasAttribute("data-other-amount-radio")
        ) {
          gaEvent({
            eventCategory: "User Flow",
            eventAction: "Changed Amount",
            eventLabel: e.target.value,
          });
        }
      });
    }
  }
}

export default CurrencySelect;
