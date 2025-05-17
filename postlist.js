// getPostList.js

function getPostList(jsonPath = '/posts/posts.json') {
  return fetch(jsonPath)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Failed to fetch post list: ${response.statusText}`);
      }
      return response.json();
    })
    .then(posts => {
      return posts.map(post => ({
        title: post.title || 'Untitled',
        image: post.image || '', // e.g. '/posts/img1.jpg'
        description: post.description || '',
        filename: post.filename || '#'
      }));
    })
    .catch(err => {
      console.error('Error loading posts:', err);
      return [];
    });
}
