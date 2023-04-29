const db = require("../models");
const Event = db.Event,
    Op = db.Sequelize.Op;

const {
    response_200,
    response_201,
    response_400,
    response_500,
} = require("../utils/response_codes");

const add_events = async (req, res) => {
    const data = req.body;

    if (data == null || data == "") {
        return response_400(res, "Didn't receive any data.");
    }

    if (!Array.isArray(data)) {
        return response_400(res, "Expected data to be an 'Array', got something else.");
    }

    try {
        for (let e of data) {
            const {
                machine_id,
                content,
                type,
                timestamp
            } = e;

            const log = await Event.create({
                machine_id,
                content,
                type,
                timestamp
            });
        }
    } catch (err) {
        return response_500(res, `Error while saving logs. ${err.message}`);
    }

    return response_201(res, "Logs saved successfully!");
};

const get_events = async (req, res) => {
    const {
        // To find logs specific to a device
        machine_id,

        // To find logs within specific time range
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
                // To find logs specific to a device
                ...(machine_id && {
                    machine_id,
                }),

                // To find logs within specific time range
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
        var data = await Event.findAll(query);

        if (data == null || data == []) {
            return response_400(res, "No logs found!");
        }
    } catch (err) {
        return response_500(res, `Error while fetching logs. ${err.message}`);
    }

    return response_200(res, "Logs fetched successfully!", data);
};

const remove_events = async (req, res) => {
    const data = req.body;

    if (data == null || data == "") {
        return response_400(res, "Didn't receive any data.");
    }

    if (!Array.isArray(data)) {
        return response_400(res, "Expected data to be an 'Array', got something else.");
    }

    try {
        const log = await Event.destroy({
            where: {
                id: {
                    [Op.in]: data,
                },
            },
        });
    } catch (err) {
        return response_500(res, `Error while removing logs. ${err.message}`);
    }

    return response_201(res, "Logs removed successfully!");
};

module.exports = {
    add_events,
    get_events,
    remove_events,
};
