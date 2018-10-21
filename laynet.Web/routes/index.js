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

        let result = await db.getLatestStockScrapingDate();
        baseDate = result.rows[0].TradeDate;
        baseDateKey = date.convertDate(baseDate);

        if (cache.todayRecommendation15Period.has(baseDateKey) === false) {
            result = await db.getTodayRecommendation(baseDate, 15);

            cache.todayRecommendation15Period.set(baseDateKey, result.rows);
        }       

        result = await db.getStockTradeAfterTheDate(cache.todayRecommendation15Period.get(baseDateKey)[0].StockCode
            , date.getDateDaysAgoFromBaseDate(baseDate, 15));

        res.render('index', {
            title: 'LAYNET', baseDate: baseDateKey
            , kospi200List: cache.kospi200, todayBestTradeList: result.rows
        });
    } catch (err) {
        next(err);
    }
});

module.exports = router;