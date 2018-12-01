const db = require('../db');
const router = require('express').Router();
const cache = require('../cache');
const date = require('../date');
const moment = require('moment');

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

        if (cache.pastRecommendationResults === null) {
            result = await db.getPastRecommendationResults();
            cache.pastRecommendationResults = result.rows;
        }

        result = await db.getStockTradeAfterTheDate(cache.todayRecommendation15Period.get(baseDateKey)[0].StockCode
            , date.getDateDaysAgoFromBaseDate(baseDate, 15));

        const stockCodeSet = new Set();

        topPastRecmdnResults = cache.pastRecommendationResults.sort((a, b) => { return b.Percentage - a.Percentage; })
            .filter((elem) => {
                if (stockCodeSet.has(elem.StockCode) === false)
                { 
                    stockCodeSet.add(elem.StockCode);
                    return true;
                }

                return false;                                
            })
            .slice(0, 8);

        res.render('index', {
            title: 'LAYNET',
            baseDate: baseDateKey,
            kospi200List: cache.kospi200,
            todayBestTradeList: result.rows,
            pastRecmdnResults: topPastRecmdnResults,
            moment: moment
        });
    } catch (err) {
        next(err);
    }
});

router.get('/past', async (req, res, next) => {
    try {
        if (cache.pastRecommendationResults === null) {
            result = await db.getPastRecommendationResults();
            cache.pastRecommendationResults = result.rows;
        }

        res.render('past', {
            title: 'LAYNET',
            pastRecmdnResults: cache.pastRecommendationResults,
            moment: moment
        });
    } catch (err) {
        next(err);
    }
});

module.exports = router;