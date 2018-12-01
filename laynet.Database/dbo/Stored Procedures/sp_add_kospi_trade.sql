CREATE PROCEDURE [dbo].[sp_add_kospi_trade] (
	@tradeDate	DATE,
	@price		DECIMAL(7,2),
	@delta		DECIMAL(7,2),
	@percentage DECIMAL(5,2),
	@volume		INT,
	@TradeMoneyMillion INT
)
AS
BEGIN

    SET NOCOUNT ON

	IF NOT EXISTS(SELECT TradeDate FROM [dbo].[KospiTrade] WHERE TradeDate = @tradeDate)
	BEGIN
		INSERT INTO [dbo].[KospiTrade](TradeDate, Price, Delta, Percentage, Volume, TradeMoneyMillion)
		 VALUES (@tradeDate, @price, @delta, @percentage, @volume, @TradeMoneyMillion)
		IF (@@ROWCOUNT = 0 OR @@ERROR <> 0)
			RETURN -1
	END

	RETURN 0
END