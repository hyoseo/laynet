CREATE PROCEDURE [dbo].[sp_get_past_recommendation_results]
AS
BEGIN
	SELECT [CompanyName], [StockCode], [BaseDate], [Period], [BasePrice], [SuccessDate],
	[DiffDays], [SuccessPrice], [Delta], [Percentage], [AnnualYeild], [KospiChangeRate]
	FROM [dbo].[PastRecommendationResults]
    IF @@ROWCOUNT = 0 OR @@ERROR <> 0
		RETURN -1

	RETURN 0
END
