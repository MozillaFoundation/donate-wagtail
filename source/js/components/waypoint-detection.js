import "intersection-observer";
import scrollama from "scrollama";

function scrollamaInit() {
  // instantiate the scrollama
  const scroller = scrollama();

  // setup the instance, pass callback functions
  scroller
    .setup({
      step: ".js-data-waypoint",
    })
    .onStepEnter((response) => {
      document
        .querySelectorAll("[data-waypoint-element]")
        .forEach((stepItem) => {
          stepItem.classList.add("hidden");
        });
    });
}

export default () => {
  if (document.querySelectorAll("[data-waypoint-element]").length) {
    scrollamaInit();
  }
};
