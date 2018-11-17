CREATE PROCEDURE [dbo].[sp_update_past_recommendation_search_date]
	@stockCode	CHAR(6),
	@baseDate	DATE,
	@period		SMALLINT,
	@searchDate DATE
AS
BEGIN
    SET NOCOUNT ON

--	IF NOT EXISTS(SELECT StockCode FROM [dbo].[PastRecommendationResults] WHERE StockCode = @stockCode AND BaseDate = @baseDate AND SuccessDate = @successDate)
	BEGIN
		UPDATE [dbo].[TodayRecommendation] SET [SearchDate] = @searchDate
		WHERE [StockCode] = @stockCode AND [BaseDate] = @baseDate AND [Period] = @period
		IF (@@ROWCOUNT = 0 OR @@ERROR <> 0)
			RETURN -1
	END

	RETURN 0
END