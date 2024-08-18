import { json } from "@remix-run/node";
import { Link, useLoaderData, Outlet } from "@remix-run/react";

import {getPosts} from "~/models/post.server"

export const loader = async () => {
  return json({posts: await getPosts()});
};


export default function Posts() {
  const { posts } = useLoaderData<typeof loader>();
  return (
    <div className="mx-auto max-w-6xl">
      <div className="grid grid-cols-4 gap-6">
        <nav className="col-span-4 md:col-span-1">
          <div className="space-y-4 sm:mx-auto sm:inline-grid sm:grid-cols-2 sm:gap-5 sm:space-y-0">
            <Link to="admin" className="flex items-center justify-center rounded-md bg-yellow-500 px-4 py-3 font-medium text-white hover:bg-yellow-600">
            Admin
          </Link>
          </div>
          <ul>
            {posts.map((post) => (
              <li key={post.document_id}>
                <Link to={post.document_id} className="text-blue-600 underline">
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
                    
