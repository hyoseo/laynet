
CREATE procedure [dbo].[sp_update_kospi200_big_players_data]
AS
BEGIN
    SET NOCOUNT ON

	DECLARE @ranking INT = 1
	DECLARE @stockCode CHAR(6)

	WHILE @ranking <= 200
	BEGIN
		SELECT @stockCode = StockCode FROM [dbo].[Kospi200] WHERE Ranking = @ranking

		EXEC sp_update_big_players_data @stockCode
	
		SET @ranking +=1 
	END

	RETURN 0
END