function convertDate(dt)
{
    day = dt.getDate();
    day = (day >= 10) ? day : '0' + day;
    month = dt.getMonth() + 1;
    month = (month >= 10) ? month : '0' + month;

    return dt.getFullYear() + '-' + month + '-' + day;
}

module.exports.convertDate = convertDate;

module.exports.getDateDaysAgoFromBaseDate = (baseDate, days) => {
    baseDate.setDate(baseDate.getDate() - days);

    return baseDate;
};

module.exports.getDateDaysAgo = days => {
    let dt = new Date();
    dt.setDate(dt.getDate() - days);

    return convertDate(dt);
};

module.exports.getDateMonthsAgo = months => {
    let dt = new Date();
    dt.setMonth(dt.getMonth() - months);

    return convertDate(dt);
};

module.exports.getDateYearsAgo = years => {
    let dt = new Date();
    dt.setFullYear(dt.getFullYear() - years);

    return convertDate(dt);
};