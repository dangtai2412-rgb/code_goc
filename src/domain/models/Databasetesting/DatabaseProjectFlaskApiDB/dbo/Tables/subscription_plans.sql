CREATE TABLE [dbo].[subscription_plans] (
    [plan_id]   INT             IDENTITY (1, 1) NOT NULL,
    [plan_name] VARCHAR (100)   NOT NULL,
    [duration]  INT             NULL,
    [price]     NUMERIC (12, 2) NULL,
    PRIMARY KEY CLUSTERED ([plan_id] ASC)
);


GO

