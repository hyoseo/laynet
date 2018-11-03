
CREATE procedure [dbo].[sp_get_past_recommendation]
AS
BEGIN

    SET NOCOUNT ON

	SELECT * FROM [dbo].[TodayRecommendation] WITH(NOLOCK) ORDER BY StockCode, BaseDate ASC
    IF @@ROWCOUNT = 0 OR @@ERROR <> 0
		RETURN -1

	RETURN 0
END
