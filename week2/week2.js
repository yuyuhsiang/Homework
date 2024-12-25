let posts = [];

        function CreatePost() {
            document.getElementById('blogList').style.display = 'none';
            document.getElementById('createPost').style.display = 'block';
        }

        function BlogList() {
            document.getElementById('blogList').style.display = 'block';
            document.getElementById('createPost').style.display = 'none';
            document.getElementById('title').value = '';
            document.getElementById('content').value = '';
        }

        function addPost() {
            const title = document.getElementById('title').value;
            const content = document.getElementById('content').value;

            if (!title || !content) {
                alert('請填寫標題和內容！');
                return;
            }

            const post = {
                title: title,
                content: content,
                date: new Date().toLocaleString('zh-TW')
            };

            posts.unshift(post);
            updatePosts();
            BlogList();
        }

        function updatePosts() {
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

        BlogList();