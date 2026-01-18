CREATE TABLE [dbo].[order_details] (
    [order_id]       INT             NOT NULL,
    [product_id]     INT             NOT NULL,
    [unit_id]        INT             NULL,
    [order_quantity] INT             NULL,
    [unit_price]     NUMERIC (12, 2) NULL,
    [line_total]     NUMERIC (12, 2) NULL,
    PRIMARY KEY CLUSTERED ([order_id] ASC, [product_id] ASC)
);


GO

