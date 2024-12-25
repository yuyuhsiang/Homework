async function loadPosts() {
    try {
        const response = await fetch('/api/posts');
        const posts = await response.json();
        updatePosts(posts);
    } catch (error) {
        console.error('Error loading posts:', error);
    }
}

function showCreatePost() {
    document.getElementById('blogList').style.display = 'none';
    document.getElementById('createPost').style.display = 'block';
}

function showBlogList() {
    document.getElementById('blogList').style.display = 'block';
    document.getElementById('createPost').style.display = 'none';
    document.getElementById('title').value = '';
    document.getElementById('content').value = '';
}

async function addPost() {
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;

    if (!title || !content) {
        alert('請填寫標題和內容！');
        return;
    }

    try {
        const response = await fetch('/api/posts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, content })
        });

        if (response.ok) {
            await loadPosts();
            showBlogList();
        } else {
            alert('發布失敗，請稍後再試！');
        }
    } catch (error) {
        console.error('Error adding post:', error);
        alert('發布失敗，請稍後再試！');
    }
}

function updatePosts(posts) {
    const postsDiv = document.getElementById('posts');
    postsDiv.innerHTML = '';

    posts.forEach(post => {
        const postElement = document.createElement('div');
        postElement.className = 'post';
        postElement.innerHTML = `
            <div class="post-title">${post.title}</div>
            <div class="post-content">${post.content}</div>
            <div class="post-date">${post.date}</div>
        `;
        postsDiv.appendChild(postElement);
    });
}

// 初始化載入貼文
document.addEventListener('DOMContentLoaded', () => {
    loadPosts();
    showBlogList();
});