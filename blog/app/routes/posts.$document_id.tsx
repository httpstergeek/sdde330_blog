import type { LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { useLoaderData, useNavigation} from "@remix-run/react";
import { marked} from "marked";
import invariant from "tiny-invariant";

import { getPost } from "~/models/post.server";

export const loader = async ({
  params,
}: LoaderFunctionArgs) => {
  invariant(params.document_id, "params.document_id is required");

  const post = await getPost(params.document_id);
  invariant(post, `Post not found: ${params.document_id}`);

  const html = marked(post.content);
  return json({ html, post });
};

export default function PostDocumentId() {
  const {html, post } = useLoaderData<typeof loader>();
  return (
    <div className="mx-auto max-w-4xl">
      <h1 className="my-6 border-b-2 text-center text-3xl">
        {post.title}
      </h1>
      <div dangerouslySetInnerHTML={{ __html: html }} />
    </div>
  );
}
