let currentCommentCount = 0;

const ws = new WebSocket("ws://127.0.0.1:9001");

// 接続が確立した時
ws.addEventListener("open", () => {
  console.log("WebSocket 接続が確立しました");
});

// メッセージを受信した時
ws.addEventListener("message", (event) => {
  console.log("サーバーからのメッセージ:", event.data);
});

// エラーが発生した時
ws.addEventListener("error", (error) => {
  console.error("WebSocket エラー:", error);
});

// 接続が閉じられた時
ws.addEventListener("close", () => {
  console.log("WebSocket 接続が閉じられました");
});

function main() {
  console.log("Starting");
}

function monitorComments() {
  let commentElements = document.getElementsByClassName("question-item__body");
  let comments = [];
  for (let i = 0; i < commentElements.length; i++) {
    comments.push(commentElements[i].childNodes[0].innerText);
  }
  sendComments(comments);
  console.log(comments);
}

function sendComments(comments) {
  ws.send(JSON.stringify(comments));
}

// 0.5秒（500ミリ秒）おきに処理を実行
const intervalId = setInterval(monitorComments, 500);

// 5秒後に停止する例
// setTimeout(() => {
//   clearInterval(intervalId);
//   console.log("処理を停止しました");
// }, 5000);

main();
