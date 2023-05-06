const log_controller = require("../controllers/log");
const express = require("express"),
    log_router = express.Router();

const multer = require("multer");
const storage = multer.diskStorage({
    destination: (req, file, callback) => {
        callback(null, "uploads/logs");
    },
    filename: (req, file, callback) => {
        const uniqueSuffix = Date.now() + "" + Math.round(Math.random() * 1E9);
        callback(null, `${file.filename}.${uniqueSuffix}`);
    }
});

const upload = multer({ storage });

module.exports = function (app) {
    log_router.get("/get", log_controller.get_logs);
    log_router.post(
        "/upload",
        upload.single("file"),
        log_controller.upload_log
    );
    log_router.delete("/remove", log_controller.remove_logs);

    app.use("/log", log_router);
};
