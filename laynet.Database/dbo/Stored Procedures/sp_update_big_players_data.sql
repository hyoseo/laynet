
CREATE procedure [dbo].[sp_update_big_players_data] (
    @stockCode CHAR(6)
) 
AS
BEGIN
    SET NOCOUNT ON

	DECLARE @companyName NVARCHAR(30)
	DECLARE @searchDate DATE 

	SELECT TOP 1 @companyName = CompanyName, @searchDate = TradeDate
	 FROM StockTradeVolume WITH(NOLOCK) WHERE StockCode = @stockCode ORDER BY TradeDate DESC
	IF @@ROWCOUNT = 0
	BEGIN
		RETURN -1
	END

	SET @searchDate = DATEADD(DAY, 1, @searchDate)

	DECLARE @curveType VARCHAR(10)
	DECLARE @stockPrice INT
	DECLARE @institutionsVolume BIGINT
	DECLARE @foreignersVolume BIGINT

	DECLARE @institutionsVolumeSum BIGINT = 0
	DECLARE @foreignersVolumeSum BIGINT = 0

	DECLARE @beforeCurveStockPrice INT = 0
	DECLARE @beforeCurveDate DATE
	DECLARE @beforeCurveInstitutionsVolumeSum BIGINT = 0
	DECLARE @beforeCurveForeignersVolumeSum BIGINT = 0

	DECLARE @curveDayDelta FLOAT = 0

	WHILE 1=1
	BEGIN
		SELECT TOP 1 @searchDate = TradeDate, @stockPrice = StockPrice, @curveType = CurveType
		, @institutionsVolume = InstitutionsVolume, @foreignersVolume = ForeignersVolume 
		FROM StockTradeVolume WITH(NOLOCK) WHERE StockCode = @stockCode AND TradeDate < @searchDate ORDER BY TradeDate DESC
		IF @@ROWCOUNT = 0
		BEGIN
			RETURN 0
		END

		IF @curveType LIKE 'CURVE%'
		BEGIN
			IF @beforeCurveStockPrice <> 0
			BEGIN
				-- 이전 커브 날짜의 CurveDelta값 업데이트
				SET @curveDayDelta = ROUND((CAST((@beforeCurveStockPrice - @stockPrice) AS FLOAT) / @stockPrice) * 100, 2)
				UPDATE [dbo].[BigPlayersData] SET CurveDelta = @curveDayDelta 
				, InstitutionsVolumeDelta = @institutionsVolumeSum - @beforeCurveInstitutionsVolumeSum
				, ForeignersVolumeDelta = @foreignersVolumeSum - @beforeCurveForeignersVolumeSum
				WHERE StockCode = @stockCode AND CurveDate = @beforeCurveDate
			END

			SET @beforeCurveDate = @searchDate
			SET @beforeCurveStockPrice = @stockPrice

			SET	@beforeCurveInstitutionsVolumeSum = @institutionsVolumeSum
			SET	@beforeCurveForeignersVolumeSum  = @foreignersVolumeSum

			IF EXISTS(SELECT @searchDate FROM [dbo].[BigPlayersData] WHERE StockCode = @stockCode AND CurveDate = @searchDate)
			BEGIN
				UPDATE [dbo].[BigPlayersData] SET 
				InstitutionsVolumeSum = @institutionsVolumeSum
				, ForeignersVolumeSum = @foreignersVolumeSum
				WHERE StockCode = @stockCode AND CurveDate = @searchDate
			END
			ELSE
			BEGIN
				INSERT INTO [dbo].[BigPlayersData] VALUES
				(@companyName, @stockCode, @searchDate, @curveType, @stockPrice, 0
				, 0, 0, @institutionsVolumeSum, @foreignersVolumeSum)
			END
		END

		SET @institutionsVolumeSum += @institutionsVolume
		SET @foreignersVolumeSum += @foreignersVolume
	END

	RETURN 0
END
