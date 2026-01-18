CREATE TABLE [dbo].[administrators] (
    [admin_id]         INT           IDENTITY (1, 1) NOT NULL,
    [admin_name]       VARCHAR (100) NOT NULL,
    [admin_permission] VARCHAR (100) NULL,
    PRIMARY KEY CLUSTERED ([admin_id] ASC)
);


GO

