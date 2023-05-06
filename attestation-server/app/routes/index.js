module.exports = (app) => {
    require("./event")(app);
    require("./log")(app);
};
