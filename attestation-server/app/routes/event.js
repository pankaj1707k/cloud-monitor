const event_controller = require("../controllers/event");
const express = require("express"),
    event_router = express.Router();

module.exports = function (app) {
    event_router.get("/get", event_controller.get_events);
    event_router.post("/add", event_controller.add_event);
    event_router.delete("/remove", event_controller.remove_events);

    app.use("/event", event_router);
};
