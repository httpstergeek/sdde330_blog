type Post = {
  content: string;
  author_id: string;
  title: string;
  blog_id: string
  document_id: string
  created_date: string
};



export async function getPosts(): Promise<Array<Post>> {
  try {
    const response = await fetch('http://localhost:8000/api/document/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: Array<Post> = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching posts:', error);
    throw error;
  }
}

export async function deletePost(document_id: string): Promise<Post> {
  console.log(document_id)
  try {
    const response = await fetch('http://localhost:8000/api/document/' + document_id, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: Post = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching posts:', error);
    throw error;
  }
}

export async function getPost(document_id: string): Promise<Post> {
  console.log(document_id)
  try {
    const response = await fetch('http://localhost:8000/api/document/' + document_id, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: Post = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching posts:', error);
    throw error;
  }
}

export async function createPost(
  post: Pick<Post, "title" | "author_id" | "blog_id" | "content">): Promise<Post> {
  
  console.log(post);
  try {
    const response = await fetch('http://localhost:8000/api/document/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(post),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: Post = await response.json();
    return data;
  } catch (error) {
    console.error('Error creating post:', error);
    throw error;
  }
}
