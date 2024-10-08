import type { ActionFunctionArgs } from "@remix-run/node";
import { json, redirect } from "@remix-run/node";
import { Form, useActionData, useNavigation } from "@remix-run/react";
import invariant from "tiny-invariant";


import { createPost } from "~/models/post.server";

export const action = async ({
  request,
}: ActionFunctionArgs) => {
  const formData = await request.formData();

  const title = formData.get("title");
  const blog_id = formData.get("blog_id");
  const author_id = formData.get("author_id");
  const content = formData.get("content");

  const errors = {
    title: title ? null : "Title is required",
    blog_id: blog_id ? null : "Blog Id is required",
    author_id: author_id ? null : "Author Id is required",
    content: content ? null : "Content is required",
  };
  const hasErrors = Object.values(errors).some(
    (errorMessage) => errorMessage
  );
  if (hasErrors) {
    return json(errors);
  }

  invariant(
    typeof title === "string",
    "title must be a string"
  );
  invariant(
    typeof blog_id === "string",
    "blog_id must be a string"
  );
  invariant(
    typeof author_id === "string",
    "author_id must be a string"
  );
  invariant(
    typeof content === "string",
    "content must be a string"
  );

  await createPost({ title, author_id, blog_id, content });
  return redirect("/posts/admin");
};

const inputClassName =
  "w-full rounded border border-gray-500 px-2 py-1 text-lg";

export default function NewPost() {
  const errors = useActionData<typeof action>();
  const navigation = useNavigation();
  const isCreating = Boolean(
    navigation.state === "submitting"
  );
  return (
    <Form method="post">
      <input type="hidden" name="author_id" value="4f22cb73-e093-479b-8d8b-2375fd16040c" />
      <input type="hidden" name="blog_id" value="7b25f93f-4b4e-41c5-bcdb-d59f3dd4a677" />
      <p>
        <label>
          Post Title:{" "}
          {errors?.title ? (
            <em className="text-red-600">{errors.title}</em>
          ) : null}
          <input type="text" name="title" className={inputClassName} />
        </label>
      </p>
      <p>
        <label htmlFor="content">Content:
          {errors?.content ? (
            <em className="text-red-600">{errors.content}</em>
          ) : null}
        </label>
        <br />
        <textarea id="content" rows={20} name="content" className={`${inputClassName} font-mono`} />
      </p>
      <p className="text-right">
        <button
          type="submit"
          className="rounded bg-blue-500 py-2 px-4 text-white hover:bg-blue-600 focus:bg-blue-400 disabled:bg-blue-300"
          disabled={isCreating}
        >
          {isCreating ? "Creating..." : "Create Post"}
        </button>
      </p>
    </Form>
  );
}
