module.exports = (sequelize, Sequelize) => {
    const Event = sequelize.define(
        "event",
        {
            machine_id: {
                type: Sequelize.STRING,
                required: true,
            },
            data: {
                type: Sequelize.JSON,
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

    return Event;
};
