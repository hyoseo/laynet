CREATE procedure [dbo].[sp_get_ex_kospi200]
AS
BEGIN

    SET NOCOUNT ON

	SELECT [CompanyName], [StockCode] FROM [dbo].[StockTradeVolume] 
	WHERE [StockCode] NOT IN (SELECT [StockCode] FROM [dbo].[Kospi200] GROUP BY [StockCode]) 
	GROUP BY [CompanyName], [StockCode]
    IF @@ROWCOUNT = 0 OR @@ERROR <> 0
		RETURN -1

	RETURN 0
END
