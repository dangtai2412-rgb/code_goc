CREATE TABLE [dbo].[products] (
    [product_id]     INT             IDENTITY (1, 1) NOT NULL,
    [owner_id]       INT             NULL,
    [product_name]   VARCHAR (100)   NOT NULL,
    [selling_price]  NUMERIC (12, 2) NULL,
    [stock_quantity] INT             NULL,
    PRIMARY KEY CLUSTERED ([product_id] ASC)
);


GO

