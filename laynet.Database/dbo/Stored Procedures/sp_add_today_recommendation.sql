CREATE procedure [dbo].[sp_add_today_recommendation] (
    @companyName NVARCHAR(30),
    @stockCode CHAR(6),
	@baseDate DATE,
	@period SMALLINT,
	@variation SMALLINT,
	@curveSimilarValue DECIMAL(3,2),
	@curveSuperiority VARCHAR(8),
	@currentSimilarValue DECIMAL(3,2),
	@currentSuperiority VARCHAR(8)
) 
AS
BEGIN

    SET NOCOUNT ON

	IF NOT EXISTS(SELECT StockCode FROM [dbo].[TodayRecommendation] WHERE StockCode = @stockCode AND BaseDate = @baseDate AND Period = @period)
	BEGIN
		INSERT INTO [dbo].[TodayRecommendation](CompanyName, StockCode, BaseDate, Period, Variation, CurveSimilarValue, CurveSuperiority, CurrentSimilarValue, CurrentSuperiority)
		 VALUES (@companyName, @stockCode, @baseDate, @period, @variation, @curveSimilarValue, @curveSuperiority, @currentSimilarValue, @currentSuperiority)
		IF (@@ROWCOUNT = 0 OR @@ERROR <> 0)
			RETURN -1
	END

	RETURN 0
END
