const db = require('../db');
const router = require('express').Router();

router.get('/', async (req, res, next) => {
    try {
        let result = await db.getKospi200();

        res.render('index', { title: 'LAYNET', kospi200List: result.rows });
    } catch (err) {
        next(err);
    }
});

module.exports = router;