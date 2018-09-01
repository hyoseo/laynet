
CREATE procedure [dbo].[sp_delete_before_split_stock] (
    @stockCode CHAR(6)
)
AS
BEGIN
    SET NOCOUNT ON
	
	DECLARE @stockPrice INT
	DECLARE @maxStockPrice INT
	DECLARE @tradeDate DATE

	SELECT TOP 1 @stockPrice = StockPrice, @tradeDate = TradeDate FROM StockTradeVolume WITH(NOLOCK) WHERE StockCode = @stockCode AND InstitutionsVolume = 0 AND ForeignersVolume = 0 ORDER BY TradeDate DESC
	IF @tradeDate IS NOT NULL
	BEGIN
		SELECT @maxStockPrice = MAX(StockPrice) FROM StockTradeVolume WITH(NOLOCK) WHERE StockCode = @stockCode AND InstitutionsVolume <> 0 AND ForeignersVolume <> 0 AND TradeDate > @tradeDate
		
		IF @maxStockPrice IS NOT NULL AND @stockPrice > @maxStockPrice * 2
		BEGIN
			DELETE FROM StockTradeVolume WHERE StockCode = @stockCode AND TradeDate <= @tradeDate
		END
	END

	RETURN 0
END
