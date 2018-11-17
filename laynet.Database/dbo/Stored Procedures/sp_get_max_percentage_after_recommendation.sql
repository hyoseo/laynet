CREATE PROCEDURE [dbo].[sp_get_max_percentage_after_recommendation]
	@stockCode CHAR(6),
	@baseDate DATE
AS
BEGIN
    SET NOCOUNT ON

	SELECT TOP 1 Percentage FROM PastRecommendationResults WHERE StockCode = @stockCode AND BaseDate = @baseDate ORDER BY Percentage DESC
    IF @@ROWCOUNT = 0 OR @@ERROR <> 0
		RETURN -1

	RETURN 0
END