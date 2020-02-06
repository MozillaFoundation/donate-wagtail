export default function fetchEnv(handleEnvData) {
  let envReq = new XMLHttpRequest();

  envReq.addEventListener("load", () => {
    let envData = {};

    try {
      envData = JSON.parse(envReq.response);
    } catch (e) {
      // discard
    }

    handleEnvData(envData);
  });

  envReq.open("GET", "/environment.json");
  envReq.send();
}
