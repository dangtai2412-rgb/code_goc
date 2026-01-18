CREATE TABLE [dbo].[orders] (
    [order_id]       INT             IDENTITY (1, 1) NOT NULL,
    [customer_id]    INT             NULL,
    [employee_id]    INT             NULL,
    [order_date]     DATE            NULL,
    [order_status]   VARCHAR (20)    NULL,
    [payment_method] VARCHAR (50)    NULL,
    [total_amount]   NUMERIC (12, 2) NULL,
    PRIMARY KEY CLUSTERED ([order_id] ASC)
);


GO

