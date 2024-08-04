CREATE DATABASE blog;
GRANT ALL PRIVILEGES ON DATABASE blog TO berniem;
CREATE TABLE users (
	user_id uuid DEFAULT gen_random_uuid(),
	username VARCHAR(50) NOT NULL,
	bio TEXT NOT NULL,
	email VARCHAR(100) NOT NULL,
	created_date TIMESTAMP NOT NULL DEFAULT NOW(),
	last_post_date TIMESTAMP,
	PRIMARY KEY (user_id)
);

CREATE TABLE blogs (
	blog_id uuid DEFAULT gen_random_uuid(),
	title VARCHAR(100) NOT NULL,
	creator_id uuid,
	created_date TIMESTAMP NOT NULL DEFAULT NOW(),
	last_post_date TIMESTAMP,
	CONSTRAINT fk_creator_id FOREIGN KEY(creator_id) REFERENCES users(user_id),
	PRIMARY KEY (blog_id)
);

CREATE TABLE blog_documents (
	document_id uuid DEFAULT gen_random_uuid(),
	title VARCHAR(100) NOT NULL,
	content TEXT NOT NULL,
	created_date TIMESTAMP NOT NULL DEFAULT NOW(),
	author_id uuid NOT NULL,
	blog_id uuid NOT NULL,
	CONSTRAINT fk_author_id FOREIGN KEY(author_id) REFERENCES users(user_id),
	CONSTRAINT fk_blog_id FOREIGN KEY(blog_id) REFERENCES blogs(blog_id),
	PRIMARY KEY (document_id)
);

CREATE TABLE comments (
	comment_id uuid DEFAULT gen_random_uuid(),
	parent_comment_id uuid,
	content TEXT NOT NULL,
	created_date TIMESTAMP NOT NULL DEFAULT NOW(),
	author_id uuid NOT NULL,
	document_id uuid NOT NULL,
	CONSTRAINT fk_parent_comment_id FOREIGN KEY(parent_comment_id) REFERENCES comments(comment_id),
	CONSTRAINT fk_author_id FOREIGN KEY(author_id) REFERENCES users(user_id),
	CONSTRAINT fk_document_id FOREIGN KEY(document_id) REFERENCES blog_documents(document_id),
	PRIMARY KEY (comment_id)
);
