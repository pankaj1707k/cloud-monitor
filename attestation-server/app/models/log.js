module.exports = (sequelize, Sequelize) => {
    const Log = sequelize.define(
        "log",
        {
            machine_id: {
                type: Sequelize.STRING,
            },
            content: {
                type: Sequelize.STRING,
            },
            type: {
                type: Sequelize.STRING,
            },
            timestamp: {
                type: Sequelize.INTEGER,
            },
            log_filepath: {
                type: Sequelize.STRING,
            },
        },
        {
            timestamps: false,
        }
    );

    return Log;
};
