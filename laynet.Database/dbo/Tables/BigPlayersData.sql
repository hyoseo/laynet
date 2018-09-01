CREATE TABLE [dbo].[BigPlayersData] (
    [CompanyName]             NVARCHAR (30) NOT NULL,
    [StockCode]               CHAR (6)      NOT NULL,
    [CurveDate]               DATE          NOT NULL,
    [CurveType]               VARCHAR (10)  NOT NULL,
    [StockPrice]              INT           NOT NULL,
    [CurveDelta]              FLOAT (53)    NOT NULL,
    [MoneyDelta]              BIGINT        NOT NULL,
    [InstitutionsMoneyDelta]  BIGINT        NOT NULL,
    [ForeignersMoneyDelta]    BIGINT        NOT NULL,
    [MoneySum]                BIGINT        NOT NULL,
    [InstitutionsMoneySum]    BIGINT        NOT NULL,
    [ForeignersMoneySum]      BIGINT        NOT NULL,
    [VolumeDelta]             BIGINT        NOT NULL,
    [InstitutionsVolumeDelta] BIGINT        NOT NULL,
    [ForeignersVolumeDelta]   BIGINT        NOT NULL,
    [VolumeSum]               BIGINT        NOT NULL,
    [InstitutionsVolumeSum]   BIGINT        NOT NULL,
    [ForeignersVolumeSum]     BIGINT        NOT NULL,
    CONSTRAINT [PK_BigPlayersTotalMoney] PRIMARY KEY CLUSTERED ([StockCode] ASC, [CurveDate] ASC)
);

