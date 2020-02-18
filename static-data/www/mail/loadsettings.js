mailSettings = {}

fetch('/config/get/mail', {
    headers: {
      "content-type": "application/json",
      "token": webpass
    }})
.then((resp) => resp.json())
.then(function(settings) {
    mailSettings = settings || {}
    if (mailSettings.default_forward_secrecy === false){
        document.getElementById('forwardSecrecySetting').checked = false
    }
  })