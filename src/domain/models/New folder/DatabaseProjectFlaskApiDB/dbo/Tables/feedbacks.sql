CREATE TABLE [dbo].[feedbacks] (
    [id]            INT           IDENTITY (1, 1) NOT NULL,
    [feedback_text] VARCHAR (255) NULL,
    [evaluation]    FLOAT (53)    NULL,
    [created_at]    DATETIME      NULL,
    [updated_at]    DATETIME      NULL,
    [course_id]     INT           NULL,
    [user_id]       INT           NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    FOREIGN KEY ([course_id]) REFERENCES [dbo].[courses] ([id]),
    FOREIGN KEY ([user_id]) REFERENCES [dbo].[flask_user] ([id])
);


GO

