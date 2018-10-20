const db = require('../db');
const router = require('express').Router();
const cache = require('../cache');
const date = require('../date');

router.get('/', async (req, res, next) => {
    try {
        if (cache.kospi200 === null) {
            let result = await db.getKospi200();
            cache.kospi200 = result.rows;
        }

        baseDate = date.getDateDaysAgo(4);
        if (cache.todayRecommendation15Period.has(baseDate) === false) {
            let result = await db.getTodayRecommendation(baseDate, 15);

            cache.todayRecommendation15Period.set(baseDate, result.rows);
        }

        let result = await db.getStockTradeAfterTheDate(cache.todayRecommendation15Period.get(baseDate)[0].StockCode, date.getDateDaysAgo(19));

        res.render('index', { title: 'LAYNET', baseDate: baseDate, kospi200List: cache.kospi200, todayBestTradeList: result.rows });
    } catch (err) {
        next(err);
    }
});

module.exports = router;