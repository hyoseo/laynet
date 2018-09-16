
CREATE PROCEDURE [dbo].[sp_get_stock_trade_after_the_date]
	@stockCode CHAR(6),
	@date DATE
AS
BEGIN

    SET NOCOUNT ON

	SELECT * FROM [dbo].[StockTradeVolume] WHERE StockCode = @stockCode AND TradeDate > @date ORDER BY TradeDate DESC
    IF @@ROWCOUNT = 0 OR @@ERROR <> 0
		RETURN -1

	RETURN 0
END
