
CREATE procedure [dbo].[sp_delete_all_before_split_stock] 
AS
BEGIN
    SET NOCOUNT ON

	DECLARE @stopTradingTopPrice TABLE(
		number INT IDENTITY(1, 1),
		stockCode CHAR(6),
		stockPrice INT
	)

	DECLARE @count INT = 1
	DECLARE @maxCount INT

	DECLARE @stockCode CHAR(6)
	DECLARE @stockPrice INT
	DECLARE @maxStockPrice INT
	DECLARE @tradeDate DATE

	INSERT INTO @stopTradingTopPrice SELECT StockCode, StockPrice FROM StockTradeVolume WITH(NOLOCK) WHERE InstitutionsVolume = 0 AND ForeignersVolume = 0 GROUP BY StockCode, StockPrice

	SELECT @maxCount = MAX(number) FROM @stopTradingTopPrice

	WHILE @count <= @maxCount
	BEGIN
		SELECT @stockCode = stockCode, @stockPrice = stockPrice FROM @stopTradingTopPrice WHERE number = @count
	
		SELECT TOP 1 @tradeDate = TradeDate FROM StockTradeVolume WITH(NOLOCK) WHERE StockCode = @stockCode AND InstitutionsVolume = 0 AND ForeignersVolume = 0 ORDER BY TradeDate DESC

		SELECT @maxStockPrice = MAX(StockPrice) FROM StockTradeVolume WITH(NOLOCK) WHERE StockCode = @stockCode AND InstitutionsVolume <> 0 AND ForeignersVolume <> 0 AND TradeDate > @tradeDate

		IF @maxStockPrice IS NOT NULL AND @stockPrice > @maxStockPrice * 2
		BEGIN
			DELETE FROM StockTradeVolume WHERE StockCode = @stockCode AND TradeDate <= @tradeDate
		END

		SET @count = @count + 1
	END

	RETURN 0
END
