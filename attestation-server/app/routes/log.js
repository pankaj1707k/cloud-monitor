const log_controller = require("../controllers/log");
const express = require("express"),
    log_router = express.Router();

module.exports = function (app) {
    log_router.get("/get", log_controller.get_logs);
    log_router.post("/add", log_controller.add_logs);
    log_router.delete("/remove", log_controller.remove_logs);

    app.use("/log", log_router);
};
