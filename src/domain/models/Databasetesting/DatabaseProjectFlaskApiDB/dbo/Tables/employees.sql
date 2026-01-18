CREATE TABLE [dbo].[employees] (
    [employee_id]   INT           IDENTITY (1, 1) NOT NULL,
    [owner_id]      INT           NULL,
    [employee_name] VARCHAR (100) NOT NULL,
    [role]          VARCHAR (50)  NULL,
    [active_status] BIT           NULL,
    PRIMARY KEY CLUSTERED ([employee_id] ASC)
);


GO

