const db = require('../db');
const date = require('../date');
const router = require('express').Router();

router.get('/:stockcode', async (req, res, next) => {
    try {
        let result = await db.getStockTradeAfterTheDate(req.params.stockcode, date.getDateMonthsAgo(1));

        res.render('stock', { title: result.rows[0].CompanyName, tradeList: result.rows });
    } catch (err) {
        next(err);
    }
});

module.exports = router;