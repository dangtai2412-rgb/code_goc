CREATE TABLE [dbo].[customers] (
    [customer_id]            INT             IDENTITY (1, 1) NOT NULL,
    [customer_name]          VARCHAR (100)   NOT NULL,
    [phone_number]           VARCHAR (20)    NULL,
    [address]                VARCHAR (200)   NULL,
    [total_outstanding_debt] NUMERIC (12, 2) NULL,
    PRIMARY KEY CLUSTERED ([customer_id] ASC)
);


GO

