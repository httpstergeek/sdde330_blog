import type { ActionFunctionArgs } from "@remix-run/node";
import { redirect } from "@remix-run/node";
import { json } from "@remix-run/node";
import { Link, Outlet, useLoaderData } from "@remix-run/react";

import { getPosts } from "~/models/post.server";
import { createPost } from "~/models/post.server";

export const action = async ({
  request,
}: ActionFunctionArgs) => {
  const formData = await request.formData();

  const title = formData.get("title");
  const blog_id = formData.get("blog_id");
  const content = formData.get("content");
  console.log(title, blog_id, content)
  await createPost({ title, blog_id, content });

  return redirect("/posts/admin");
};

export const loader = async () => {
  return json({ posts: await getPosts() });
};

export default function PostAdmin() {
  const { posts } = useLoaderData<typeof loader>();
  return (
    <div className="mx-auto max-w-6xl">
      <h1 className="my-6 mb-2 border-b-2 text-center text-3xl">
        Blog Admin
      </h1>
      <div className="grid grid-cols-4 gap-6">
        <nav className="col-span-4 md:col-span-1">
          <div className="space-y-4 sm:mx-auto sm:inline-grid sm:grid-cols-2 sm:gap-5 sm:space-y-0">
            <Link to="new" className="flex items-center justify-center rounded-md bg-yellow-500 px-4 py-3 font-medium text-white hover:bg-yellow-600">
              New Post
            </Link>
          </div>
          <ul>
            {posts.map((post) => (
              <li key={post.document_id}>
                <Link
                  to={post.document_id}
                  className="text-blue-600 underline"
                >
                  {post.title}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
        <main className="col-span-4 md:col-span-3">
	    <Outlet />
        </main>
      </div>
    </div>
  );
}
