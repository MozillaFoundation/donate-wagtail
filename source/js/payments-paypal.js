import initPaypal from "./components/paypal";
import expectRecaptcha from "./components/recaptcha";

function setupBraintree() {
  var donateForm = document.querySelector(`.layout .donate-form`),
    donationPending = document.querySelector(".layout .donatation-pending"),
    paymentForm = document.getElementById("payments__braintree-form"),
    nonceInput = document.getElementById("id_braintree_nonce"),
    amountInput = document.getElementById("id_amount"),
    frequencyInput = document.getElementById("id_frequency"),
    currencyInput = document.getElementById("id_currency"),
    captchaInput = document.getElementById("id_captcha"),
    captchaEnabled = captchaInput !== null,
    currencySelect = document.getElementById("id_currency-switcher-currency");

  var getCurrency = () => currencySelect.value.toUpperCase();

  var getAmountSingle = () => {
    var donateForm = document.getElementById("donate-form--single");
    return donateForm.querySelector('input[name="amount"]:checked').value;
  };

  var onAuthorizeSingle = (payload) => {
    nonceInput.value = payload.nonce;
    amountInput.value = getAmountSingle();
    frequencyInput.value = "single";
    currencyInput.value = currencySelect.value;
    if (captchaEnabled) {
      expectRecaptcha(window.grecaptcha.execute);
    } else {
      submitForm();
    }
  };

  var getAmountMonthly = () => {
    var donateForm = document.getElementById("donate-form--monthly");
    return donateForm.querySelector('input[name="amount"]:checked').value;
  };

  var onAuthorizeMonthly = (payload) => {
    nonceInput.value = payload.nonce;
    amountInput.value = getAmountMonthly();
    frequencyInput.value = "monthly";
    currencyInput.value = currencySelect.value;
    if (captchaEnabled) {
      expectRecaptcha(window.grecaptcha.execute);
    } else {
      submitForm();
    }
  };

  initPaypal(
    getAmountSingle,
    getCurrency,
    onAuthorizeSingle,
    "checkout",
    "#payments__paypal-button--single"
  );

  initPaypal(
    getAmountMonthly,
    getCurrency,
    onAuthorizeMonthly,
    "vault",
    "#payments__paypal-button--monthly"
  );

  function submitForm() {
    donateForm.classList.add("hidden");
    if (donationPending) {
      donationPending.classList.remove("hidden");
    } else {
      console.warn(`payment-pending view missing`);
    }
    paymentForm.submit();
  }

  // Set up recaptcha
  expectRecaptcha(() => {
    const recaptcha = document.getElementById("g-recaptcha");
    const props = {
      sitekey: recaptcha.dataset.publicKey,
      size: "invisible",
      callback: (token) => {
        try {
          captchaInput.value = token;
          submitForm();
        } catch (err) {
          console.error(err);
        }
      },
    };

    grecaptcha.render("g-recaptcha", props);
  });
}

function toggle(overlay, input) {
  let value = parseFloat(input.value);
  let valid = input.reportValidity() && !isNaN(value);

  overlay.style.display = valid ? "none" : "block";
}

function setupPaypalOverlays() {
  let overlays = document.querySelectorAll(
    ".payments__button--paypal--overlay"
  );
  overlays.forEach((overlay) => {
    let form = overlay.closest("form");
    let inputs = Array.from(
      form.querySelectorAll("[type=radio][name=amount],[type=number]")
    );

    inputs.forEach((input) => {
      // Anytime an input is selected, check whether that means we need to "lock" the
      // paypal button with a click-intercepting overlay.
      input.addEventListener("input", (_) => toggle(overlay, input));
      input.addEventListener("focus", (_) => toggle(overlay, input));
    });

    // also get the currency label, because it's "clickable".
    let otherLabel = form.querySelector(".donation-amount-other__label");
    let otherInput = document.getElementById(otherLabel.getAttribute("for"));

    otherLabel.addEventListener("click", (_) => toggle(overlay, otherInput));

    overlay.addEventListener("click", () => {
      // The fact that this function fires at all means the current value is not a
      // valid value. Force the form to report this the same way it reports everything else.
      form.reportValidity();
    });
  });
}

document.addEventListener("DOMContentLoaded", function () {
  const payPalButtons = document.querySelectorAll(`.payments__button--paypal`);

  if (payPalButtons.length > 0) {
    setupBraintree();
    setupPaypalOverlays();
  }
});
