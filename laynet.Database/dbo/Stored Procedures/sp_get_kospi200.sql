
CREATE procedure [dbo].[sp_get_kospi200]
AS
BEGIN

    SET NOCOUNT ON

	SELECT * FROM [dbo].[Kospi200] ORDER BY Ranking
    IF @@ROWCOUNT = 0 OR @@ERROR <> 0
		RETURN -1

	RETURN 0
END
