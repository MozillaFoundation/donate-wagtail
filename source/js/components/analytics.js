export default function gaEvent(params) {
  if (typeof ga === "function") {
    params["transport"] = "beacon";
    ga("send", "event", params);
  }
}
