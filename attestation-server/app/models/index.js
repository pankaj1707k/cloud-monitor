const config = require("../config/db.js");
const Sequelize = require("sequelize");

const sequelize = new Sequelize(config.DATABASE_URL, {
    dialect: config.dialect,
    pool: {
        max: config.pool.max,
        min: config.pool.min,
        acquire: config.pool.acquire,
        idle: config.pool.idle,
    },
    logging: config.logging,
});

module.exports = {
    // Database ORM Object
    sequelize,
    Sequelize,

    // Models
    Event: require("./event")(sequelize, Sequelize),
    Log: require("./log")(sequelize, Sequelize),
};
