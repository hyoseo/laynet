
CREATE PROCEDURE [dbo].[sp_get_big_players_data_after_the_date]
	@stockCode CHAR(6),
	@date DATE
AS
BEGIN
	SELECT * FROM [dbo].[BigPlayersData] WHERE StockCode = @stockCode AND CurveDate > @date ORDER BY CurveDate DESC
    IF @@ROWCOUNT = 0 OR @@ERROR <> 0
		RETURN -1

	RETURN 0

END
