CREATE TABLE [dbo].[courses] (
    [id]          INT           IDENTITY (1, 1) NOT NULL,
    [course_name] VARCHAR (255) NOT NULL,
    [description] VARCHAR (255) NULL,
    [status]      VARCHAR (50)  NOT NULL,
    [start_date]  DATETIME      NOT NULL,
    [end_date]    DATETIME      NOT NULL,
    [created_at]  DATETIME      NULL,
    [updated_at]  DATETIME      NULL,
    PRIMARY KEY CLUSTERED ([id] ASC)
);


GO

