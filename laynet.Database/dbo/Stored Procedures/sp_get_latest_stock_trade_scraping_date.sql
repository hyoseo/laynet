CREATE PROCEDURE [dbo].[sp_get_latest_stock_trade_scraping_date]
AS
BEGIN

    SET NOCOUNT ON

	SELECT TOP 1 TradeDate FROM StockTradeVolume WITH(NOLOCK) ORDER BY TradeDate DESC
    IF @@ROWCOUNT = 0 OR @@ERROR <> 0
		RETURN -1

	RETURN 0
END
