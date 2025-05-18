// getPostList.js

function getPostList(jsonPath = '/posts/postlist.json') {
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
        filename: post.filename || '#',
		alt: post.alt || ''
      }));
    })
    .catch(err => {
      console.error('Error loading posts:', err);
      return [];
    });
}

function renderPostList(posts, containerId) {
	const container = document.getElementById(containerId);
	if (!container) {
		console.error(`Element with ID "${containerId}" not found.`);
		return;
	}

	posts.forEach(post => {
		const el = document.createElement('div');
		el.classList.add('post-box');
		el.innerHTML = `
			<a href="${post.filename}">
				<h3>${post.title}</h3>
				<img src="${post.image}" alt="${post.alt}" style="max-width: 100%; height: auto;" />
				<p>${post.description}</p>
			</a>
		`;
		container.appendChild(el);
	});
}

