const db = require("../models");
const Alert = db.Alert,
    Op = db.Sequelize.Op;

const {
    response_200,
    response_201,
    response_400,
    response_500,
} = require("../utils/response_codes");

const add_alerts = async (req, res) => {
    const data = req.body;

    if (data == null || data == "") {
        return response_400(res, "Didn't receive any data.");
    }

    if (!Array.isArray(data)) {
        return response_400(
            res,
            "Expected data to be an 'Array', got something else."
        );
    }

    try {
        for (let e of data) {
            const { machine_id, subject, reason, type, timestamp } = e;

            const alert = await Alert.create({
                machine_id,
                subject,
                reason,
                type,
                timestamp,
            });
        }
    } catch (err) {
        return response_500(res, `Error while saving alerts. ${err.message}`);
    }

    return response_201(res, "Alerts saved successfully!");
};

const get_alerts = async (req, res) => {
    // To fetch specific alert by ID
    const { id } = req.query;

    if (id != undefined && id != null && id != "") {
        try {
            var alert = await Alert.findByPk(id);

            if (alert == null) {
                return response_400(res, "No alert found!");
            }
        } catch (err) {
            return response_500(
                res,
                `Error while fetching alert. ${err.message}`
            );
        }

        return response_200(res, "Alert fetched successfully!", alert);
    }

    const {
        // To find alerts specific to a device
        machine_id,

        // To find alerts within specific time range
        min_timestamp,
        max_timestamp,
    } = req.query;

    var {
        // To sort by specific field
        sort_field,
        sort_order,

        // To paginate the response
        page,
        size,
    } = req.query;

    // Set the default fields
    sort_field ||= "timestamp";
    sort_order ||= "ASC";
    page ||= 1;
    size ||= 8;

    // Create the query
    const query = {
        where: {
            [Op.and]: {
                // To find alerts specific to a device
                ...(machine_id && {
                    machine_id,
                }),

                // To find alerts within specific time range
                ...((min_timestamp || max_timestamp) && {
                    timestamp: {
                        ...(min_timestamp && {
                            [Op.gte]: min_timestamp,
                        }),
                        ...(max_timestamp && {
                            [Op.lte]: max_timestamp,
                        }),
                    },
                }),
            },
        },

        // To sort by specific field
        order: [[sort_field, sort_order]],

        // To paginate the response
        ...(page > 0 && {
            limit: size,
            offset: (page - 1) * size,
        }),
    };

    try {
        var data = await Alert.findAll(query);

        if (data == null || data == []) {
            return response_400(res, "No alerts found!");
        }
    } catch (err) {
        return response_500(res, `Error while fetching alerts. ${err.message}`);
    }

    return response_200(res, "Alerts fetched successfully!", data);
};

const remove_alerts = async (req, res) => {
    const data = req.body;

    if (data == null || data == "") {
        return response_400(res, "Didn't receive any data.");
    }

    if (!Array.isArray(data)) {
        return response_400(
            res,
            "Expected data to be an 'Array', got something else."
        );
    }

    try {
        await Alert.destroy({
            where: {
                id: {
                    [Op.in]: data,
                },
            },
        });
    } catch (err) {
        return response_500(res, `Error while removing alerts. ${err.message}`);
    }

    return response_201(res, "Alerts removed successfully!");
};

module.exports = {
    add_alerts,
    get_alerts,
    remove_alerts,
};
