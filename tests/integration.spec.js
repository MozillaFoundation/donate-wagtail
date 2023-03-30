const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("./wait-for-images.js");

test(`Donate homepage`, async ({ page }, _testInfo) => {
  page.on(`console`, console.log);
  await page.goto(`http://localhost:8000/en-US/`);
  await waitForImagesToLoad(page);

  const logo = await page.locator(`a.header__logo-link`);
  expect(await logo.isVisible()).toBe(true);


  // The tests below have been commented out because we are no longer using our 
  // HTML donate form. Instead, we are using a FundraiseUp form component that is loaded in through javascript. 
  // See: https://github.com/MozillaFoundation/foundation.mozilla.org/issues/10261

  // // default view is single
  // const form = await page.locator(`.donate-form--single`);
  // expect(await form.isVisible()).toBe(true);

  // values match expected values - TODO: figure out how we can marry python constants with JS testing
  // const inputs = await page.locator(
  //   `#donate-form--single .donation-amount input`
  // );
  // const values = [];
  // const count = await inputs.count();
  // for (let i = 0; i < count; ++i) {
  //   values[i] = parseFloat(await inputs.nth(i).inputValue());
  // }
  // expect(values).toEqual([10, 20, 30, 60, NaN, NaN]);
});
