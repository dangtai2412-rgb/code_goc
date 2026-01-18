CREATE TABLE [dbo].[debts] (
    [debt_id]           INT             IDENTITY (1, 1) NOT NULL,
    [order_id]          INT             NULL,
    [customer_id]       INT             NULL,
    [debt_amount]       NUMERIC (12, 2) NULL,
    [debt_created_date] DATE            NULL,
    [debt_status]       VARCHAR (20)    NULL,
    PRIMARY KEY CLUSTERED ([debt_id] ASC)
);


GO

