class DonationCurrencyWidth {
  static selector() {
    return "[data-donation-currency]";
  }

  constructor(node) {
    this.node = node;
    this.getWidth();
  }

  getWidth() {
    // Set custom css property to give padding on slide
    this.currencyWidth = this.node.getBoundingClientRect();
    document.documentElement.style.setProperty(
      "--currency-width",
      this.currencyWidth.width + "px"
    );
  }
}

export default DonationCurrencyWidth;
