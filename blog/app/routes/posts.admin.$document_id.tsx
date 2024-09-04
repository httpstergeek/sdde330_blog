import type { LoaderFunctionArgs } from "@remix-run/node";
import { json, ActionFunctionArgs, redirect } from "@remix-run/node";
import { Form, useLoaderData, useActionData, useNavigation } from "@remix-run/react";
import invariant from "tiny-invariant";

import { getPost, updatePost, deletePost } from "~/models/post.server";

export const action = async ({
  request,
}: ActionFunctionArgs) => {
  const formData = await request.formData();
  const intent = formData.get("intent");
  const title = formData.get("title");
  const blog_id = formData.get("blog_id");
  const author_id = formData.get("author_id");
  const content = formData.get("content");
  const document_id = formData.get("document_id");

  if (intent === "delete") {
      invariant(typeof document_id === "string", "document_id must be a string");
      await deletePost(document_id);
      return redirect("/posts/admin");
    }

  const errors = {
    title: title ? null : "Title is required",
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
    typeof document_id === "string",
    "document_id must be a string"
  );
  invariant(
    typeof author_id === "string",
    "author_id must be a string"
  );
  invariant(
    typeof content === "string",
    "content must be a string"
  );
  await updatePost({ title, author_id, blog_id, document_id, content });
  return redirect("/posts/admin");
};

export const loader = async ({
  params,
}: LoaderFunctionArgs) => {
  invariant(params.document_id, "params.document_id is required");

  const post = await getPost(params.document_id);
  invariant(post, `Post not found: ${params.document_id}`);
  return json({ ...post, document_id: params.document_id });
};
const inputClassName =
  "w-full rounded border border-gray-500 px-2 py-1 text-lg";

export default function PostDocumentId() {
  const post  = useLoaderData<typeof loader>();
  const errors = useActionData<typeof action>();
  const navigation = useNavigation();
  const isCreating = Boolean(
    navigation.state === "submitting"
  );
  return (
    <Form method="post">
      <input type="hidden" name="document_id" className={inputClassName} value={post.document_id} />
      <input type="hidden" name="author_id" value="4f22cb73-e093-479b-8d8b-2375fd16040c" />
      <input type="hidden" name="blog_id" value="7b25f93f-4b4e-41c5-bcdb-d59f3dd4a677" />
      <p>
        <label>
          Post Title:{" "}
          {errors?.title ? (
            <em className="text-red-600">{errors.title}</em>
          ) : null}
          <input type="text" name="title" className={inputClassName} defaultValue={post.title} />
        </label>
      </p>
      <p>
        <label htmlFor="content">Content:
          {errors?.content ? (
            <em className="text-red-600">{errors.content}</em>
          ) : null}
        </label>
        <br />
        <textarea id="content" rows={20} name="content" className={`${inputClassName} font-mono`} defaultValue={post?.content || ""} />
      </p>
      <div className="space-y-4 sm:mx-auto sm:inline-grid sm:grid-cols-2 sm:gap-5 sm:space-y-0">
        <p className="text-right">
          <button
            type="submit"
            name="intent"
            value="delete"
            className="rounded bg-red-500 py-2 px-4 text-white hover:bg-blue-600 focus:bg-blue-400 disabled:bg-blue-300"
            disabled={isCreating}
          >
          {isCreating ? "Deleting..." : "Delete"}
          </button>
        </p>
        <p className="text-right">
          <button
            type="submit"
            name="intent"
            value="update"
            className="rounded bg-blue-500 py-2 px-4 text-white hover:bg-blue-600 focus:bg-blue-400 disabled:bg-blue-300"
            disabled={isCreating}
          >
            {isCreating ? "Updating..." : "Update Post"}
          </button>
        </p>
      </div>
    </Form>
  );}

