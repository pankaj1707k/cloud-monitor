module.exports = (sequelize, Sequelize) => {
    const Alert = sequelize.define(
        "alert",
        {
            machine_id: {
                type: Sequelize.STRING,
            },
            subject: {
                type: Sequelize.STRING,
            },
            reason: {
                type: Sequelize.STRING,
            },
            type: {
                type: Sequelize.STRING,
            },
            timestamp: {
                type: Sequelize.INTEGER,
            },
        },
        {
            timestamps: false,
        }
    );

    return Alert;
};
