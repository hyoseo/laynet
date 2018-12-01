CREATE procedure [dbo].[sp_get_latest_kospi_trade_date] 
AS
BEGIN
    SET NOCOUNT ON

	DECLARE @searchDate DATE 

	SELECT TOP 1 @searchDate = [TradeDate] FROM [dbo].[KospiTrade] ORDER BY TradeDate DESC
    IF @@ROWCOUNT = 0 OR @@ERROR <> 0
	BEGIN
		SELECT TOP 1 @searchDate = [BaseDate] FROM [dbo].[TodayRecommendation] ORDER BY BaseDate ASC
		IF @@ROWCOUNT = 0 OR @@ERROR <> 0
			RETURN -1
	END

	SELECT @searchDate

	RETURN 0
END
