let express = require("express");
let app = express();
let path = require("path");
const PORT = 8181;

app.use(express.static("./public"));

app.get("/", function (req, res) {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.get("/about", function (req, res) {
  res.sendFile(path.join(__dirname, "about.html"));
});

app.listen(PORT);

console.log(`Server started at localhost:${PORT}`);
