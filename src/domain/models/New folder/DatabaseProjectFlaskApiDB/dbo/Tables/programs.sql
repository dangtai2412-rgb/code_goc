CREATE TABLE [dbo].[programs] (
    [id]          INT           IDENTITY (1, 1) NOT NULL,
    [title]       VARCHAR (255) NOT NULL,
    [description] VARCHAR (255) NULL,
    [status]      VARCHAR (50)  NOT NULL,
    [created_at]  DATETIME      NULL,
    [updated_at]  DATETIME      NULL,
    PRIMARY KEY CLUSTERED ([id] ASC)
);


GO

