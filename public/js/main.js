// const url = "http://0.0.0.0:8080";
const url = "/backend";
const ending = "…";
let endingLength = ending.length;
let count = 0;

const buttons = Array.from(document.getElementsByClassName("start"));
const holder = document.getElementById("holder");
const counter = document.getElementById("counter");
const allEqual = (arr) => arr.every((v) => v === arr[0]);

async function start() {
  let initialButtonJson = await getData(`${url}/start`);

  buttons.forEach(function (button, idx) {
    button.innerText = `${initialButtonJson.prompts[idx]}${ending}`;
    button.classList.remove("is-loading");

    button.onclick = async function (event) {
      let el = event.currentTarget;

      counter.innerText = ++count;
      buttons.forEach(function (button) {
        button.classList.add("is-loading");
      });

      let buttonText = el.innerText.slice(0, -endingLength);
      let span = createSpan(buttonText);

      // first button click
      if (count == 1) {
        holder.replaceChild(span, holder.childNodes[0]);
      } else {
        holder.appendChild(span);
      }

      setFlash(span);

      // story continuation text
      let promptJson = await postData(`${url}/prompt`, {
        prefix: holder.innerText,
      });
      span = createSpan(promptJson.prompt);
      holder.appendChild(span);
      setFlash(span);

      // generate buttons
      let generatedJson = await postData(`${url}/generate`, {
        prefix: holder.innerText,
      });

      // occasionally all button texts are the same. render inline and try again
      while (allEqual(generatedJson.prompts)) {
        span = createSpan(generatedJson.prompts[0]);
        holder.appendChild(span);
        setFlash(span);

        generatedJson = await postData(`${url}/generate`, {
          prefix: holder.innerText,
        });
      }

      Array.prototype.forEach.call(buttons, async function (button, idx) {
        button.innerText = `${generatedJson.prompts[idx]}${ending}`;
        button.classList.remove("is-loading");
      });
    };
  });
}

async function getData(url, method) {
  let response = await fetch(url);

  if (response.ok) {
    return await response.json();
  } else {
    console.error("HTTP-Error: " + response.status);
    return {};
  }
}

async function postData(url, data) {
  let response = await fetch(url, {
    method: "POST",
    body: JSON.stringify(data),
  });

  if (response.ok) {
    return await response.json();
  } else {
    console.error("HTTP-Error: " + response.status);
    return {};
  }
}

function createSpan(text) {
  // create a new span element
  let newSpan = document.createElement("span");
  // and give it some content
  let newContent = document.createTextNode(text);
  // add the text node to the newly created span
  newSpan.appendChild(newContent);

  return newSpan;
}

function setFlash(span) {
  span.classList.add("flash");
  setTimeout(function () {
    span.classList.remove("flash");
  }, 6000);
}

window.addEventListener("DOMContentLoaded", start);
