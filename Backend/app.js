const express = require("express");
const cors = require("cors");
const app = express();
const port = 3000;

app.use(express.json());
app.options("/", cors());
// app.use(cors());

const pdfRouter = require("./routes/pdf/genPdf");
app.use("/", pdfRouter);

app.listen(port, () => {
  console.log(`App listening on port ${port}.`);
});
