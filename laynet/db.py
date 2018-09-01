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
