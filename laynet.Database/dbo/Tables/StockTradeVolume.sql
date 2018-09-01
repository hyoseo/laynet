CREATE TABLE [dbo].[StockTradeVolume] (
    [CompanyName]        NVARCHAR (30) NOT NULL,
    [StockCode]          CHAR (6)      NOT NULL,
    [TradeDate]          DATE          NOT NULL,
    [StockPrice]         INT           NOT NULL,
    [Delta]              INT           NOT NULL,
    [CurveType]          VARCHAR (10)  NOT NULL,
    [InstitutionsVolume] INT           NOT NULL,
    [ForeignersVolume]   INT           NOT NULL,
    CONSTRAINT [PK_StockTradeVolume] PRIMARY KEY CLUSTERED ([StockCode] ASC, [TradeDate] ASC)
);

