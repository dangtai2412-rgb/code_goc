CREATE TABLE [dbo].[units] (
    [unit_id]         INT             IDENTITY (1, 1) NOT NULL,
    [product_id]      INT             NULL,
    [unit_name]       VARCHAR (100)   NOT NULL,
    [conversion_rate] NUMERIC (10, 4) NULL,
    [is_base_unit]    BIT             NULL,
    PRIMARY KEY CLUSTERED ([unit_id] ASC)
);


GO

