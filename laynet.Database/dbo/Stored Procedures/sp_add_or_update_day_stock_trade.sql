
CREATE procedure [dbo].[sp_add_or_update_day_stock_trade] (
    @companyName NVARCHAR(30),
    @stockCode CHAR(6),
	@tradeDate DATE,
	@stockPrice INT,
	@delta INT,
	@curveType VARCHAR(10),
	@institutionsVolume INT,
	@foreignersVolume INT
) 
AS
BEGIN

    SET NOCOUNT ON

	IF NOT EXISTS(SELECT StockCode FROM [dbo].[StockTradeVolume] WHERE StockCode = @stockCode AND TradeDate = @tradeDate)
	BEGIN
		INSERT INTO [dbo].[StockTradeVolume](CompanyName, StockCode, TradeDate, StockPrice, Delta, CurveType, InstitutionsVolume, ForeignersVolume)
		 VALUES (@companyName, @stockCode, @tradeDate, @stockPrice, @delta, @curveType, @institutionsVolume, @foreignersVolume)
		IF (@@ROWCOUNT = 0 OR @@ERROR <> 0)
			RETURN -1
	END
	ELSE
	BEGIN
		UPDATE [dbo].[StockTradeVolume] SET CurveType = @curveType WHERE StockCode = @stockCode AND TradeDate = @tradeDate
	END

	RETURN 0
END
