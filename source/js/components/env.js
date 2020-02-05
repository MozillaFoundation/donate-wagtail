export default function fetchEnv(callback) {
  let envReq = new XMLHttpRequest();

  envReq.addEventListener("load", () => {
    let envData;

    try {
      envData = JSON.parse(envReq.response);
    } catch (e) {
      // discard
    }

    callback(envData);
  });

  envReq.open("GET", "/environment.json");
  envReq.send();
}
