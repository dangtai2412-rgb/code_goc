CREATE TABLE [dbo].[course_register] (
    [id]        INT IDENTITY (1, 1) NOT NULL,
    [user_id]   INT NULL,
    [course_id] INT NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    FOREIGN KEY ([course_id]) REFERENCES [dbo].[courses] ([id]),
    FOREIGN KEY ([user_id]) REFERENCES [dbo].[flask_user] ([id])
);


GO

