module.exports = (app) => {
    require("./alert")(app);
    require("./event")(app);
    require("./log")(app);
};
