CREATE TABLE [dbo].[appointments] (
    [id]            INT           IDENTITY (1, 1) NOT NULL,
    [consultant_id] INT           NULL,
    [user_id]       INT           NULL,
    [description]   VARCHAR (255) NULL,
    [status]        VARCHAR (50)  NOT NULL,
    [start_time]    DATETIME      NOT NULL,
    [end_time]      DATETIME      NOT NULL,
    [url_online]    VARCHAR (255) NULL,
    [created_at]    DATETIME      NULL,
    [updated_at]    DATETIME      NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    FOREIGN KEY ([consultant_id]) REFERENCES [dbo].[consultants] ([id]),
    FOREIGN KEY ([user_id]) REFERENCES [dbo].[flask_user] ([id])
);


GO

