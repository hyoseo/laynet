import pyodbc
import config

def connect():
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+config.SQLSERVER+';DATABASE='+config.DATABASE+';UID='+config.USERNAME+';PWD='+ config.PASSWORD)
    cnxn.autocommit = True
    return cnxn.cursor()

def addOrUpdateKospi200(ranking, companyName, stockCode, marketSum, askingPriceUnit):
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_add_or_update_kospi200]
        @ranking =?
      , @companyName =?
      , @stockCode =?
      , @marketSum =?
      , @askingPriceUnit =?;
    SELECT @rv AS return_value;
    """
    params = (ranking, companyName, stockCode, marketSum, askingPriceUnit)

    cursor.execute(sql, params)
    return_value = cursor.fetchval()

    return return_value

def addOrUpdateDayStockTrade(companyName, stockCode, tradeDate, stockPrice, delta, curveType, institutionsVolume, foreignersVolume):
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_add_or_update_day_stock_trade]
        @companyName =?
      , @stockCode =?
      , @tradeDate =?
      , @stockPrice =?
      , @delta =?
      , @curveType =?
      , @institutionsVolume =?
      , @foreignersVolume =?;
    SELECT @rv AS return_value;
    """
    params = (companyName, stockCode, tradeDate, stockPrice, delta, curveType, institutionsVolume, foreignersVolume)

    cursor.execute(sql, params)
    return_value = cursor.fetchval()

    return return_value

def getLatestStockTrade(stockCode):
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_get_latest_stock_trade]
        @stockCode =?;
    SELECT @rv AS return_value;
    """

    cursor.execute(sql, stockCode)
    row = cursor.fetchone()
    cursor.nextset()
    
    if cursor.fetchval() == -1:
        return None

    return row

def getLatestStockTradeDate(stockCode):
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_get_latest_stock_trade_date]
        @stockCode =?;
    SELECT @rv AS return_value;
    """

    cursor.execute(sql, stockCode)
    row = cursor.fetchone()
    cursor.nextset()
    
    if cursor.fetchval() == -1:
        return None

    return row[0]

def getKospi200():
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_get_kospi200];
    SELECT @rv AS return_value;
    """

    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.nextset()

    if cursor.fetchval() == -1:
        return None

    return rows

def deleteAllBeforeSplitStock():
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_delete_all_before_split_stock];
    SELECT @rv AS return_value;
    """

    cursor.execute(sql)

    if cursor.fetchval() == -1:
        return False

    return True

def deleteBeforeSplitStock(stockCode):
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_delete_before_split_stock]
        @stockCode =?;
    SELECT @rv AS return_value;
    """

    cursor.execute(sql, stockCode)

    if cursor.fetchval() == -1:
        return False

    return True
def updateBigPlayersData(stockCode):
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_update_big_players_data]
        @stockCode =?;
    SELECT @rv AS return_value;
    """

    cursor.execute(sql, stockCode)

    if cursor.fetchval() == -1:
        return False

    return True
def getBigPlayersDataAfterTheDate(stockCode, date):
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_get_big_players_data_after_the_date]
        @stockCode =?
      , @date =?;
    SELECT @rv AS return_value;
    """
    params = (stockCode, date)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    cursor.nextset()

    if cursor.fetchval() == -1:
        return None

    return rows
def getStockTradeAfterTheDate(stockCode, date):
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_get_stock_trade_after_the_date]
        @stockCode =?
      , @date =?;
    SELECT @rv AS return_value;
    """
    params = (stockCode, date)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    cursor.nextset()

    if cursor.fetchval() == -1:
        return None

    return rows

def addTodayRecommendation(companyName, stockCode, baseDate, period, basePrice, variation, curveSimilarValue, curveSuperiority, currentSimilarValue, currentSuperiority, searchDate):
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_add_today_recommendation]
        @companyName =?
      , @stockCode =?
      , @baseDate =?
      , @period =?
      , @basePrice =?
      , @variation =?
      , @curveSimilarValue =?
      , @curveSuperiority =?
      , @currentSimilarValue =?
      , @currentSuperiority =?
      , @searchDate =?;
    SELECT @rv AS return_value;
    """
    params = (companyName, stockCode, baseDate, period, basePrice, variation, curveSimilarValue, curveSuperiority, currentSimilarValue, currentSuperiority, searchDate)

    cursor.execute(sql, params)
    return_value = cursor.fetchval()

    return return_value

def getLatestStockScrapingDate():
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_get_latest_stock_trade_scraping_date];
    SELECT @rv AS return_value;
    """

    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.nextset()
    
    if cursor.fetchval() == -1:
        return None

    return row[0]

def getPastRecommendation():
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_get_past_recommendation];
    SELECT @rv AS return_value;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.nextset()

    if cursor.fetchval() == -1:
        return None

    return rows

def addPastRecommendationResults(companyName, stockCode, baseDate, period, basePrice, successDate, successPrice, kospiChangeRate):
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_add_past_recommendation_results]
        @companyName =?
      , @stockCode =?
      , @baseDate =?
      , @period =?
      , @basePrice =?
      , @successDate =?
      , @successPrice =?
      , @kospiChangeRate =?;
    SELECT @rv AS return_value;
    """

    params = (companyName, stockCode, baseDate, period, basePrice, successDate, successPrice, kospiChangeRate)

    cursor.execute(sql, params)
    return_value = cursor.fetchval()

    return return_value

def getMaxPercentageAfterRecommendation(stockCode, baseDate):
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_get_max_percentage_after_recommendation]
        @stockCode =?
      , @baseDate =?;
    SELECT @rv AS return_value;
    """

    params = (stockCode, baseDate)

    cursor.execute(sql, params)
    row = cursor.fetchone()
    cursor.nextset()
    
    if cursor.fetchval() == -1:
        return None

    return row[0]

def updatePastRecommendationSearchDate(stockCode, baseDate, period, searchDate):
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_update_past_recommendation_search_date]
        @stockCode =?
      , @baseDate =?
      , @period =?
      , @searchDate =?;
    SELECT @rv AS return_value;
    """
    params = (stockCode, baseDate, period, searchDate)

    cursor.execute(sql, params)
    return_value = cursor.fetchval()

    return return_value

def getLatestKospiTradeDate():
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_get_latest_kospi_trade_date];
    SELECT @rv AS return_value;
    """

    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.nextset()
    
    if cursor.fetchval() == -1:
        return None

    return row[0]

def addKospiTrade(tradeDate, price, delta, percentage, volume, TradeMoneyMillion):
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_add_kospi_trade]
        @tradeDate =?
      , @price =?
      , @delta =?
      , @percentage =?
      , @volume =?
      , @TradeMoneyMillion =?;
    SELECT @rv AS return_value;
    """
    params = (tradeDate, price, delta, percentage, volume, TradeMoneyMillion)

    cursor.execute(sql, params)
    return_value = cursor.fetchval()

    return return_value

def getKospiTradeAfterFirstRecommendation():
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_get_kospi_trade_after_first_recommendation];
    SELECT @rv AS return_value;
    """

    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.nextset()

    if cursor.fetchval() == -1:
        return None

    return rows

def getExKospi200():
    cursor = connect()

    sql = """\
    DECLARE @rv INT;
    EXEC @rv = [dbo].[sp_get_ex_kospi200];
    SELECT @rv AS return_value;
    """

    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.nextset()

    if cursor.fetchval() == -1:
        return None

    return rows
