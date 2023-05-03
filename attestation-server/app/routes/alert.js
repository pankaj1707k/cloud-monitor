const alert_controller = require("../controllers/alert");
const express = require("express"),
    alert_router = express.Router();

module.exports = function (app) {
    alert_router.get("/get", alert_controller.get_alerts);
    alert_router.post("/add", alert_controller.add_alert);
    alert_router.delete("/remove", alert_controller.remove_alerts);

    app.use("/alert", alert_router);
};
