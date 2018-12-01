const sql = require('mssql');
const config = require('./config');

module.exports.getKospi200 = async () => {
    try {
        let pool = await new sql.ConnectionPool(config.db).connect();

        let result = await pool.request().execute('sp_get_kospi200');
        if (result.returnValue === -1) {
            throw result.result;
        }

        sql.close();

        return {
            returnValue: result.returnValue,
            rows: result.recordset
        };
    } catch (err) {
        sql.close();

        throw err;
    }
};

module.exports.getLatestStockTrade = async stockCode => {
    try {
        let pool = await new sql.ConnectionPool(config.db).connect();

        let result = await pool.request()
            .input('stockCode', sql.Char(6), stockCode)
            .execute('sp_get_latest_stock_trade');
        if (result.returnValue === -1) {
            throw result.result;
        }

        sql.close();

        return {
            returnValue: result.returnValue,
            rows: result.recordset
        };
    } catch (err) {
        sql.close();

        throw err;
    }
};

module.exports.getStockTradeAfterTheDate = async (stockCode, date) => {
    try {
        let pool = await new sql.ConnectionPool(config.db).connect();

        let result = await pool.request()
            .input('stockCode', sql.Char(6), stockCode)
            .input('date', sql.Date, date)
            .execute('sp_get_stock_trade_after_the_date');
        if (result.returnValue === -1) {
            throw result.result;
        }

        sql.close();
        
        return {
            returnValue: result.returnValue,
            rows: result.recordset
        };
    } catch (err) {
        sql.close();

        throw err;
    }
};

module.exports.getBigPlayersDataAfterTheDate = async (stockCode, date) => {
    try {
        let pool = await new sql.ConnectionPool(config.db).connect();

        let result = await pool.request()
            .input('stockCode', sql.Char(6), stockCode)
            .input('date', sql.Date, date)
            .execute('sp_get_big_players_data_after_the_date');
        if (result.returnValue === -1) {
            throw result.result;
        }

        sql.close();

        return {
            returnValue: result.returnValue,
            rows: result.recordset
        };
    } catch (err) {
        sql.close();

        throw err;
    }
};

module.exports.getTodayRecommendation = async (baseDate, period) => {
    try {
        let pool = await new sql.ConnectionPool(config.db).connect();

        let result = await pool.request()
            .input('baseDate', sql.Date, baseDate)
            .input('period', sql.SmallInt, period)
            .execute('sp_get_today_recommendation');
        if (result.returnValue === -1) {
            throw result.result;
        }

        sql.close();

        return {
            returnValue: result.returnValue,
            rows: result.recordset
        };
    } catch (err) {
        sql.close();

        throw err;
    }
};

module.exports.getLatestStockScrapingDate = async () => {
    try {
        let pool = await new sql.ConnectionPool(config.db).connect();

        let result = await pool.request()
            .execute('sp_get_latest_stock_trade_scraping_date');
        if (result.returnValue === -1) {
            throw result.result;
        }

        sql.close();

        return {
            returnValue: result.returnValue,
            rows: result.recordset
        };
    } catch (err) {
        sql.close();

        throw err;
    }
};

module.exports.getPastRecommendationResults = async () => {
    try {
        let pool = await new sql.ConnectionPool(config.db).connect();

        let result = await pool.request().execute('sp_get_past_recommendation_results');
        if (result.returnValue === -1) {
            throw result.result;
        }

        sql.close();

        return {
            returnValue: result.returnValue,
            rows: result.recordset
        };
    } catch (err) {
        sql.close();

        throw err;
    }
};
