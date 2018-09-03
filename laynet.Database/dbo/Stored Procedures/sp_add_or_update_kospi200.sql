
CREATE procedure [dbo].[sp_add_or_update_kospi200] (
	@ranking TINYINT,
    @companyName VARCHAR(30),
    @stockCode CHAR(6),
	@marketSum BIGINT,
	@askingPriceUnit SMALLINT
) 
AS
BEGIN
    SET NOCOUNT ON

	IF NOT EXISTS(SELECT Ranking FROM [dbo].[Kospi200] WHERE Ranking = @ranking)
	BEGIN
		INSERT INTO [dbo].[Kospi200] VALUES (@ranking, @companyName, @stockCode, @marketSum, @askingPriceUnit)
		IF (@@ROWCOUNT = 0 OR @@ERROR <> 0)
			RETURN -1
	END
	ELSE
	BEGIN
		UPDATE [dbo].[Kospi200] SET CompanyName = @companyName, StockCode = @stockCode
		, MarketSum = @marketSum, AskingPriceUnit = @askingPriceUnit WHERE Ranking = @ranking
		IF (@@ERROR <> 0)
			RETURN -1
	END

	RETURN 0
END
