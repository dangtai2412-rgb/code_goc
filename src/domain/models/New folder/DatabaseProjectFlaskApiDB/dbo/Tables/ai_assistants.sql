CREATE TABLE [dbo].[ai_assistants] (
    [ai_id]               INT           IDENTITY (1, 1) NOT NULL,
    [version]             VARCHAR (20)  NULL,
    [supported_languages] VARCHAR (100) NULL,
    [ai_model_type]       VARCHAR (50)  NULL,
    PRIMARY KEY CLUSTERED ([ai_id] ASC)
);


GO

