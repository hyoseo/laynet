function convertDateToMonthDays(dt) {
    dt = new Date(dt);
    day = dt.getDate();
    day = (day >= 10) ? day : '0' + day;
    month = dt.getMonth() + 1;
    month = (month >= 10) ? month : '0' + month;

    return month + '/' + day;
};
