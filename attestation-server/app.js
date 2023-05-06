const express = require("express");
const app = express(),
    api_router = express.Router();

const server = require("http").createServer(app);
const sio = require("socket.io")(server);

const cors = require("cors");
const body_parser = require("body-parser");

// Load the project specific environment variables
require("dotenv").config();

var corsOptions = {
    origin: [
        "http://localhost:8080",
        "http://ubuntu-attestation-server-vm:8080",
    ],
    credentials: true, // Access-Control-Allow-Credentials: true
    optionSuccessStatus: 200,
};

// Connect to the database
const db = require("./app/models");

// Re-synchronize with the database to detect and make modifications
db.sequelize.sync({ alter: true }).then(() => {
    console.log("Re-synchronizing with the database ...");
});

// Serve the uploaded files at `/uploads`
app.use("/uploads", express.static(__dirname + "/uploads"));

// Set the basic middleware(s)
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(body_parser.json());
app.use(body_parser.urlencoded({ extended: true }));
app.use(cors(corsOptions));

// Root route to check if API is running or not
app.get("/", (req, res) => {
    res.json({ message: "Hurrah! API is running." });
});

// Attach all API routes to the API router
require("./app/routes")(api_router);

// Attach the API router to the `/` (root) URL path
app.use("/api", api_router);

const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

// Error handler
app.use((err, req, res, next) => {
    console.log(err);
});

sio.on("connection", (socket) => {
    // Log the received connection
    console.log(`Connected, socketID: ${socket.id}`);

    // Attach a disconnect listener when the agent disconnects
    socket.on("disconnect", () => {
        // Log the lost connection
        console.log(`Disconnected, socketID: ${socket.id}`);
    });

    // Attach socket.io event handlers
    require("./app/routes/socketio")(socket);
})