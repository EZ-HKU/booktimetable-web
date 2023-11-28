const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");


// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "https://openaiapi-site.azureedge.net/public-assets/d/76ef6eb916/favicon.svg";
const PERSON_IMG = "https://image.flaticon.com/icons/svg/145/145867.svg";
const BOT_NAME = "BOT";
const PERSON_NAME = "User";

msgerForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  botResponse(msgText);
  msgerInput.value = "";

  
});

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

function botResponse(m) {
  var url = window.location.origin + "/postchat";
  var httpRequest = new XMLHttpRequest();
  httpRequest.open("POST", url, true);
  httpRequest.setRequestHeader("Content-type", "application/json");
  var obj = {
    msg: m,
  };

  httpRequest.send(JSON.stringify(obj));

  // 响应后的回调函数
  httpRequest.onreadystatechange = function () {
    if (httpRequest.readyState == 4 && httpRequest.status == 200) {
      var json = httpRequest.responseText;
      appendMessage(BOT_NAME, BOT_IMG, "left", json);
    }
  };
  //   const r = random(0, BOT_MSGS.length - 1);
  //   const msgText = BOT_MSGS[r];
  //   const delay = msgText.split(" ").length * 100;


    
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}
