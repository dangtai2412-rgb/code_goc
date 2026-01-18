CREATE TABLE [dbo].[flask_user] (
    [id]          INT           IDENTITY (1, 1) NOT NULL,
    [user_name]   VARCHAR (18)  NOT NULL,
    [password]    VARCHAR (18)  NOT NULL,
    [description] VARCHAR (255) NULL,
    [status]      BIT           NOT NULL,
    [created_at]  DATETIME      NULL,
    [updated_at]  DATETIME      NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([user_name] ASC)
);


GO

