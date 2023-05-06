const socketio_controller = require("../controllers/socketio");

module.exports = function (socket) {
    socketio_controller.handle_socket(socket);
};
