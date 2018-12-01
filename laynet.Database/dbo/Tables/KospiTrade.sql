CREATE TABLE [dbo].[KospiTrade]
(
    [TradeDate]			DATE NOT NULL,
	[Price]				DECIMAL(7,2) NOT NULL,
    [Delta]				DECIMAL(7,2) NOT NULL,
	[Percentage]		DECIMAL(5,2) NOT NULL,
	[Volume]			INT NOT NULL,
	[TradeMoneyMillion] INT NOT NULL,
    CONSTRAINT [PK_KospiTrade] PRIMARY KEY CLUSTERED ([TradeDate])
)
