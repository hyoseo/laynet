
CREATE procedure [dbo].[sp_get_latest_stock_trade] (
	@stockCode CHAR(6)
)
AS
BEGIN

    SET NOCOUNT ON

	SELECT TOP 1 CompanyName, StockCode, TradeDate, StockPrice, Delta
	, CurveType, InstitutionsVolume, ForeignersVolume FROM [dbo].[StockTradeVolume] WHERE StockCode = @stockCode ORDER BY TradeDate DESC
    IF @@ROWCOUNT = 0 OR @@ERROR <> 0
		RETURN -1

	RETURN 0
END
