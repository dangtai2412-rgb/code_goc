CREATE TABLE [dbo].[business_owners] (
    [owner_id]       INT           IDENTITY (1, 1) NOT NULL,
    [owner_name]     VARCHAR (100) NOT NULL,
    [phone_number]   VARCHAR (20)  NULL,
    [email]          VARCHAR (100) NULL,
    [account_status] VARCHAR (20)  NULL,
    [admin_id]       INT           NULL,
    [plan_id]        INT           NULL,
    PRIMARY KEY CLUSTERED ([owner_id] ASC)
);


GO

