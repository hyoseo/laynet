CREATE PROCEDURE [dbo].[sp_add_past_recommendation_results]
    @companyName NVARCHAR(30),
    @stockCode CHAR(6),
	@baseDate DATE,
	@period SMALLINT,
	@basePrice INT,
	@successDate DATE,
	@successPrice INT,
	@kospiChangeRate DECIMAL(4,1)
AS
BEGIN
    SET NOCOUNT ON
	
	IF NOT EXISTS(SELECT StockCode FROM [dbo].[PastRecommendationResults] WHERE StockCode = @stockCode AND BaseDate = @baseDate AND SuccessDate = @successDate)
	BEGIN
		INSERT INTO [dbo].[PastRecommendationResults](CompanyName, StockCode, BaseDate, Period, BasePrice, SuccessDate, SuccessPrice, KospiChangeRate)
		VALUES (@companyName, @stockCode, @baseDate, @period, @basePrice, @successDate, @successPrice, @kospiChangeRate)
		IF (@@ROWCOUNT = 0 OR @@ERROR <> 0)
			RETURN -1
	END

	RETURN 0
END