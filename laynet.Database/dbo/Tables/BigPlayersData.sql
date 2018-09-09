CREATE TABLE [dbo].[BigPlayersData] (
    [CompanyName]             NVARCHAR (30) NOT NULL,
    [StockCode]               CHAR (6)      NOT NULL,
    [CurveDate]               DATE          NOT NULL,
    [CurveType]               VARCHAR (10)  NOT NULL,
    [StockPrice]              INT           NOT NULL,
    [CurveDelta]              FLOAT (53)    NOT NULL,
    [VolumeDelta]             AS [InstitutionsVolumeDelta] + [ForeignersVolumeDelta],
    [InstitutionsVolumeDelta] BIGINT        NOT NULL,
    [ForeignersVolumeDelta]   BIGINT        NOT NULL,
    [VolumeSum]               AS [InstitutionsVolumeSum] + [ForeignersVolumeSum],
    [InstitutionsVolumeSum]   BIGINT        NOT NULL,
    [ForeignersVolumeSum]     BIGINT        NOT NULL,
    CONSTRAINT [PK_BigPlayersTotalMoney] PRIMARY KEY CLUSTERED ([StockCode] ASC, [CurveDate] ASC)
);

