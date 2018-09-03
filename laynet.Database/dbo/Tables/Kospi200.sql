CREATE TABLE [dbo].[Kospi200] (
    [Ranking]         TINYINT       NOT NULL,
    [CompanyName]     NVARCHAR (30) NOT NULL,
    [StockCode]       CHAR (6)      NOT NULL,
    [MarketSum]       BIGINT		NOT NULL,
    [AskingPriceUnit] SMALLINT      NOT NULL,
    CONSTRAINT [PK_Kospi200] PRIMARY KEY CLUSTERED ([Ranking] ASC, [StockCode] ASC)
);

