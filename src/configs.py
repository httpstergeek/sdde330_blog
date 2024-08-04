import configparser

tags = {
    "openapi_tags": [
        {
            "name": "blog",
            "description": "This resource repersents Blog Spaces. Use it to get, crate,  find. Blog Spaces are not indented to be deleted.",
        },
        {
            "name": "users",
            "description": "This resource represents Blog Users. Use this to create and update users. Also get documents, comments, and blog spaces created by user.",
        },
        {
            "name": "comments",
            "description": "This resource represents comments. Use this to create and get comments by id.",
        },
        {
            "name": "documents",
            "description": "This resource represents blog documents. Use this to create, update, delete, and search blog documents.",
        },
    ]
}

cfg = configparser.ConfigParser()
cfg.read("blog.conf")

SERVER = server_info = dict(cfg.items("API")) | tags
DB = connection_info = dict(cfg.items("DB"))
