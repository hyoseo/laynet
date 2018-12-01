CREATE PROCEDURE [dbo].[sp_get_kospi_trade_after_first_recommendation]
AS
BEGIN
    SET NOCOUNT ON

	SELECT [TradeDate], [Price], [Delta], [Percentage], [Volume], [TradeMoneyMillion] FROM [dbo].[KospiTrade] 
	WHERE TradeDate >= (SELECT TOP 1 [BaseDate] FROM [dbo].[TodayRecommendation] ORDER BY [BaseDate] ASC) ORDER BY TradeDate ASC
    IF @@ROWCOUNT = 0 OR @@ERROR <> 0
		RETURN -1

	RETURN 0
END