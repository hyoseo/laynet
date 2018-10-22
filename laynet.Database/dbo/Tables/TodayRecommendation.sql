CREATE TABLE [dbo].[TodayRecommendation]
(
    [CompanyName]				NVARCHAR (30)	NOT NULL,
    [StockCode]					CHAR (6)		NOT NULL,
	[BaseDate]					DATE			NOT NULL,
	[Period]					SMALLINT		NOT NULL,
    [BasePrice]					INT				NOT NULL,
	[Variation]					SMALLINT		NOT NULL,
	[CurveSimilarValue]			DECIMAL(3,2)	NOT NULL,
	[CurveSuperiority]			VARCHAR(8)		NOT NULL,
	[CurrentSimilarValue]		DECIMAL(3,2)	NOT NULL,
	[CurrentSuperiority]		VARCHAR(8)		NOT NULL,
	[CurveCurrentSimilarDiff]	AS [CurveSimilarValue] - [CurrentSimilarValue],
	[SearchDate]				DATE			NOT NULL,
    CONSTRAINT [PK_TodayRecommendation] PRIMARY KEY CLUSTERED ([StockCode] ASC, [BaseDate] DESC, [Period] ASC)
)
