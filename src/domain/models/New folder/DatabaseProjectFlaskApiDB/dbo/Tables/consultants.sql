CREATE TABLE [dbo].[consultants] (
    [id]              INT           IDENTITY (1, 1) NOT NULL,
    [consultant_name] VARCHAR (255) NOT NULL,
    [description]     VARCHAR (255) NULL,
    [status]          VARCHAR (50)  NOT NULL,
    [gender]          VARCHAR (10)  NOT NULL,
    [age]             INT           NOT NULL,
    [created_at]      DATETIME      NULL,
    [updated_at]      DATETIME      NULL,
    PRIMARY KEY CLUSTERED ([id] ASC)
);


GO

