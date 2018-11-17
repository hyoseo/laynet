CREATE TABLE [dbo].[PastRecommendationResults]
(
    [CompanyName]				NVARCHAR (30)	NOT NULL,
    [StockCode]					CHAR (6)		NOT NULL,
	[BaseDate]					DATE			NOT NULL,
	[Period]					SMALLINT		NOT NULL,
    [BasePrice]					INT				NOT NULL,
	[SuccessDate]				DATE			NOT NULL,
	[DiffDays]					AS DATEDIFF(DD, BaseDate, SuccessDate),
    [SuccessPrice]				INT				NOT NULL,
	[Delta]						AS [SuccessPrice] - [BasePrice],
	[Percentage]				AS CAST(([SuccessPrice] - [BasePrice]) / CONVERT(DECIMAL, [BasePrice]) * 100 AS DECIMAL(5, 1)),
	[AnnualYeild]				AS CAST((360 / CONVERT(DECIMAL, DATEDIFF(DD, BaseDate, SuccessDate)) * CAST(([SuccessPrice] - [BasePrice]) / CONVERT(DECIMAL, [BasePrice]) * 100 AS DECIMAL(5, 1))) AS DECIMAL(7, 1)),
    CONSTRAINT [PK_PastRecommendationResults] PRIMARY KEY CLUSTERED ([StockCode] ASC, [BaseDate] DESC, [Period] ASC, [SuccessDate])
)