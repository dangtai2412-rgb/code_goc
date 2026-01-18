CREATE TABLE [dbo].[payments] (
    [payment_id]     INT             IDENTITY (1, 1) NOT NULL,
    [debt_id]        INT             NULL,
    [amount_paid]    NUMERIC (12, 2) NULL,
    [payment_date]   DATE            NULL,
    [payment_method] VARCHAR (50)    NULL,
    PRIMARY KEY CLUSTERED ([payment_id] ASC)
);


GO

