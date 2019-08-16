export default function expectRecaptcha(callback) {
  if (!window.grecaptcha) {
    return setTimeout(() => {
      expectRecaptcha(callback);
    }, 100);
  }

  window.grecaptcha.ready(callback);
}
