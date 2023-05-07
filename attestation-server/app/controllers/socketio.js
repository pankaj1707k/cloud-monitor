// Store socket.io sessions, machine-id -> socket
const sessions = {};
const LOGS_WINDOW = 16;

const handle_socket = async (socket) => {
    // Save the socket
    const machine_id = socket.handshake.headers["machine-id"];

    // Check if it is a machine or a client
    if (machine_id != null || machine_id != "") {
        sessions[machine_id] = {
            logs: {},
            socket,
        };
    }

    // Add event listeners
    socket.on("collect_log", collect_log);
};

const collect_log = async (machine_id, timestamp, type, data) => {
    let current_timestamp = parseInt(Date.now() / 1000.0);
    var logs = sessions[machine_id].logs;

    logs[timestamp] = {
        type,
        data
    };

    while (Object.keys(logs).length > 0) {
        let first_timestamp = Object.keys(logs)[0];

        if (current_timestamp - first_timestamp <= LOGS_WINDOW)
            break;

        delete logs[first_timestamp];
    }

    while (Object.keys(logs).length > LOGS_WINDOW) {
        let first_timestamp = Object.keys(logs)[0];
        delete logs[first_timestamp];
    }

    let socket = sessions[machine_id].socket;
    socket.server.emit("receive_logs", {
        machine_id,
        logs
    });
};

module.exports = {
    collect_log,
    handle_socket
};
