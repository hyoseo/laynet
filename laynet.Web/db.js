const sql = require('mssql');
const config = require('./config');

module.exports.getKospi200 = async () => {
    try {
        let pool = await sql.connect(config.db);

        let result = await pool.request().execute('sp_get_kospi200');

        return {
            returnValue: result.returnValue,
            rows: result.recordset
        };
    } catch (err) {
        return {
            returnValue: -1,
            result: err
        };
    }
};

module.exports.getLatestStockTrade = async stockCode => {
    try {
        let pool = await sql.connect(config.db);

        let result = await pool.request()
            .input('stockCode', sql.Char(6), stockCode)
            .execute('sp_get_latest_stock_trade');

        return {
            returnValue: result.returnValue,
            rows: result.recordset
        };
    } catch (err) {
        return {
            returnValue: -1,
            result: err
        };
    }
};

module.exports.getStockTradeAfterTheDate = async (stockCode, date) => {
    try {
        let pool = await sql.connect(config.db);

        let result = await pool.request()
            .input('stockCode', sql.Char(6), stockCode)
            .input('date', sql.Date, date)
            .execute('sp_get_stock_trade_after_the_date');

        return {
            returnValue: result.returnValue,
            rows: result.recordset
        };
    } catch (err) {
        return {
            returnValue: -1,
            result: err
        };
    }
};

module.exports.getBigPlayersDataAfterTheDate = async (stockCode, date) => {
    try {
        let pool = await sql.connect(config.db);

        let result = await pool.request()
            .input('stockCode', sql.Char(6), stockCode)
            .input('date', sql.Date, date)
            .execute('sp_get_big_players_data_after_the_date');

        return {
            returnValue: result.returnValue,
            rows: result.recordset
        };
    } catch (err) {
        return {
            returnValue: -1,
            result: err
        };
    }
};
