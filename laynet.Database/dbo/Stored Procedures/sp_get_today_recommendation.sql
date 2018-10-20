
CREATE PROCEDURE [dbo].[sp_get_today_recommendation]
	@baseDate DATE,
	@period SMALLINT
AS
BEGIN
	SELECT * FROM [dbo].[TodayRecommendation] WITH(NOLOCK) WHERE BaseDate=@baseDate AND Period=@period ORDER BY CurveCurrentSimilarDiff DESC
    IF @@ROWCOUNT = 0 OR @@ERROR <> 0
		RETURN -1

	RETURN 0

END
