const db = require('./db');
const date = require('./date');

db.getKospi200().then(result => {
    console.log(result);
});

db.getLatestStockTrade('251270').then(result => {
    console.log(result);
});

db.getStockTradeAfterTheDate('251270', date.getDateDaysAgo(14)).then(result => {
    console.log(result);
});

db.getBigPlayersDataAfterTheDate('251270', date.getDateMonthsAgo(1)).then(result => {
    console.log(result);
});
