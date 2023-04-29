module.exports = {
    DATABASE_URL: process.env.DATABASE_URL,
    dialect: "postgres",
    pool: {
        max: 5,
        min: 0,
        acquire: 30000,
        idle: 10000,
    },
    logging: console.log,
};
