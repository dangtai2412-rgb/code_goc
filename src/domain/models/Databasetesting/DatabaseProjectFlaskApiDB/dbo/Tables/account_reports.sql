CREATE TABLE [dbo].[account_reports] (
    [report_id]        INT           IDENTITY (1, 1) NOT NULL,
    [owner_id]         INT           NULL,
    [report_type]      VARCHAR (50)  NULL,
    [reporting_period] VARCHAR (100) NULL,
    [generated_date]   DATE          NULL,
    PRIMARY KEY CLUSTERED ([report_id] ASC)
);


GO

