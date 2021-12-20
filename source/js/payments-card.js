import client from "braintree-web/client";
import dataCollector from "braintree-web/data-collector";
import hostedFields from "braintree-web/hosted-fields";
import expectRecaptcha from "./components/recaptcha";
import gaEvent from "./components/analytics";

function setupBraintree() {
  var paymentForm = document.getElementById("payments__braintree-form"),
    nonceInput = document.getElementById("id_braintree_nonce"),
    deviceDataInput = document.getElementById("id_device_data"),
    captchaInput = document.getElementById("id_captcha"),
    captchaEnabled = captchaInput !== null,
    submitButton = document.getElementById("payments__payment-submit"),
    loadingErrorMsg = window.gettext(
      "An error occurred. Please reload the page or try again later."
    ),
    errorDiv = document.getElementById("payments__braintree-errors-card"),
    braintreeErrorClass = "braintree-hosted-fields-invalid",
    braintreeParams = JSON.parse(
      document.getElementById("payments__braintree-params").textContent
    );

  function showErrorMessage(msg) {
    if (errorDiv) {
      errorDiv.toggleAttribute("hidden", false);
      errorDiv.textContent = msg;
    } else {
      console.error(
        "error-feedback element appears to be missing from the page. Original error message:",
        msg
      );
    }
  }

  function clearErrorMessage() {
    if (errorDiv) {
      errorDiv.toggleAttribute("hidden", true);
      errorDiv.innerHTML = "";
    } else {
      console.error(
        "error-feedback element appears to be missing from the page."
      );
    }
  }

  function showFieldError(container) {
    container.classList.add(braintreeErrorClass);
  }

  function clearFieldError(container) {
    container.classList.remove(braintreeErrorClass);
  }

  function initHostedFields() {
    client.create({ authorization: braintreeParams.token }, function (
      clientErr,
      clientInstance
    ) {
      if (clientErr) {
        showErrorMessage(loadingErrorMsg);
        return;
      }

      dataCollector.create({ client: clientInstance, kount: true }, function (
        clientErr,
        dataCollectorInstance
      ) {
        if (clientErr) {
          showErrorMessage(loadingErrorMsg);
          return;
        }

        deviceDataInput.value = dataCollectorInstance.deviceData;
      });

      var options = {
        client: clientInstance,
        styles: {
          input: {
            "font-size": "16px",
            "font-family":
              "'Nunito Sans', 'Helvetica Neue', Helvetica, Arial, 'sans-serif'",
          },
        },
        fields: {
          number: {
            selector: "#card-number",
          },
          cvv: {
            selector: "#cvv",
          },
          expirationDate: {
            selector: "#expiration-date",
          },
        },
      };

      hostedFields.create(options, function (
        hostedFieldsErr,
        hostedFieldsInstance
      ) {
        if (hostedFieldsErr) {
          showErrorMessage(loadingErrorMsg);
          cardInputDiv.toggleAttribute("hidden", true);
          return;
        }

        hostedFieldsInstance.on("validityChange", function (event) {
          var field = event.fields[event.emittedBy];

          if (field.isValid || field.isPotentiallyValid) {
            clearFieldError(field.container);
          } else {
            showFieldError(field.container);
          }
        });

        submitButton.addEventListener("click", function (e) {
          // Trigger browser form validation
          if (
            typeof (paymentForm.reportValidity !== "undefined") &&
            !paymentForm.reportValidity()
          ) {
            return false;
          }
          e.preventDefault();
          var state = hostedFieldsInstance.getState(),
            formValid = Object.keys(state.fields).every(function (key) {
              var isValid = state.fields[key].isValid;
              if (!isValid) {
                showFieldError(state.fields[key].container);
              }
              return isValid;
            });

          if (formValid) {
            clearErrorMessage("card");
            hostedFieldsInstance.tokenize(function (tokenizeErr, payload) {
              if (tokenizeErr) {
                showErrorMessage(
                  window.gettext(
                    "There was an error processing your payment. Please try again."
                  )
                );
                return;
              }

              nonceInput.value = payload.nonce;
              if (!captchaEnabled) {
                gaEvent({
                  eventCategory: "Signup",
                  eventAction: "Submitted the Form",
                  eventLabel: "Donate",
                });
              }

              paymentForm.submit();
            });
          } else {
            showErrorMessage(
              window.gettext(
                "Some of the fields below are invalid. Please correct the invalid fields and try again."
              )
            );
          }
        });
      });
    });
  }

  initHostedFields();

  // Set up recaptcha
  expectRecaptcha(() => {
    const recaptcha = document.getElementById("g-recaptcha");
    const isInvisible = recaptcha.classList.contains("invisible-recaptcha");
    const props = {
      sitekey: recaptcha.dataset.publicKey,
      callback: (token) => {
        try {
          captchaInput.value = token;
          submitButton.removeAttribute("disabled");
        } catch (err) {
          console.error(err);
        }
      },
    };

    if (isInvisible) {
      props.size = "invisible";
    }

    grecaptcha.render("g-recaptcha", props);

    if (isInvisible) {
      grecaptcha.execute();
    }
  });
}

document.addEventListener("DOMContentLoaded", function () {
  setupBraintree();
});
