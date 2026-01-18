CREATE TABLE [dbo].[ai_draft_orders] (
    [draft_id]            INT           IDENTITY (1, 1) NOT NULL,
    [employee_id]         INT           NULL,
    [ai_id]               INT           NULL,
    [customer_id]         INT           NULL,
    [recognized_content]  VARCHAR (MAX) NULL,
    [confirmation_status] VARCHAR (20)  NULL,
    [source]              VARCHAR (50)  NULL,
    PRIMARY KEY CLUSTERED ([draft_id] ASC)
);


GO

