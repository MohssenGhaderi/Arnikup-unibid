if (window.location.protocol == "https:") {
    var ws_scheme = "wss://";
    }
  else {
    var ws_scheme = "ws://"
};
var SERVERSOCKET_RECEIVE = ws_scheme + location.host + "/receive";
var SERVERSOCKET_SUBMIT = ws_scheme + location.host + "/submit";
var MAXTIMERSET = 10;
