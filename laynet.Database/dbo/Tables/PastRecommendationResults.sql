CREATE TABLE [dbo].[PastRecommendationResults]
(
    [CompanyName]				NVARCHAR (30)	NOT NULL,
    [StockCode]					CHAR (6)		NOT NULL,
	[BaseDate]					DATE			NOT NULL,
	[Period]					SMALLINT		NOT NULL,
    [BasePrice]					INT				NOT NULL,
	[SuccessDate]				DATE			NOT NULL,
    [SuccessPrice]				INT				NOT NULL,
	[Delta]						AS [SuccessPrice] - [BasePrice],
	[Percentage]				AS CAST(([SuccessPrice] - [BasePrice]) / CONVERT(DECIMAL, [BasePrice]) * 100 AS DECIMAL(5, 1)),
    CONSTRAINT [PK_PastRecommendationResults] PRIMARY KEY CLUSTERED ([StockCode] ASC, [BaseDate] DESC, [Period] ASC, [SuccessDate])
)
