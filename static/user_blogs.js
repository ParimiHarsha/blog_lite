Vue.component('blogs',
    {
        template: `
            <div>
            <div v-for="blog in blogs" :key="blog.id" class="card">
            <h3>{{ blog.title }}</h3>
            <img v-bind:src="'/static/' + blog.image_url" class="card-img-top" alt="{{ blog.title }}">
            <p class="card-text">{{ blog.caption }}</p>
            <p>By {{ blog.user.username }} on {{ blog.updated_at }}</p>
        
            <button  v-if="blog.user.id == current_user.id" type="button" class="btn btn-primary btn sm" data-toggle="modal" data-target="#blogModal">
                Edit
            </button>
        
            <div class="modal" id="blogModal" tabindex="-1" role="dialog">
                <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                    <h5 class="modal-title">{{ modalTitle }}</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    </div>
                    <div class="modal-body">
                    <form>
                        <div class="form-group">
                        <label for="title">Title</label>
                        <input type="text" class="form-control" id="title" :value="blog.title">
                        </div>
                        <div class="form-group">
                        <label for="caption">Caption</label>
                        <textarea class="form-control" id="caption" rows="3" :value='blog.caption'></textarea>
                        </div>
                        <div class="form-group">
                        <label for="image_url">Image URL</label>
                        <input type="text" class="form-control" id="image_url" :value="blog.image_url">
                        </div>
                    </form>
                    </div>
                    <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" @click="editBlog(blog)" data-dismiss="modal">Save</button>
                    </div>
                </div>
                </div>
            </div>
            <button v-if="blog.user.id == current_user.id" @click="deleteBlog(blog)" class="btn btn-danger btn sm">Delete</button>
            </div>
            <button @click="exportBlogs(blog)" class="btn btn-danger btn sm">Export Blogs</button>
        </div>
    `,
        data: (instance) => ({

            blogs: [],
            user_blogs: [],
            auth_token: temp,
            current_user: Object,
        }),
        props: {
            user_id: {}
        },
        mounted: function () {
            this.getCurrentUser();
            let self = this;
            this.fetchBlogs(self.user_id);
        },
        methods: {
            async getCurrentUser() {
                return fetch("http://127.0.0.1:8080/api/current-user", {
                    headers: {
                        "Content-type": "application/json",
                        "Authentication-Token": this.auth_token,
                    },
                    method: "GET",
                })
                    .then((response) => response.json())
                    .then((response) => {
                        this.current_user = response
                        return response;
                    })
                    .catch((error) => {
                        console.log(error);
                    });

            },
            fetchBlogs(id) {
                const response = fetch(`http://127.0.0.1:8080/api/blogs?user_id=${id}`, {
                    headers: {
                        "Content-type": "application/json",
                        "Authentication-Token": this.auth_token
                    },
                    method: "GET",
                }).then((response) => response.json())
                    .then(response => {
                        var user_blogs = [];
                        this.blogs = response.blogs;
                        for (let blog in this.blogs) {
                            if (this.blogs[blog].user.id == this.user_id) {
                                user_blogs.push(this.blogs[blog]);
                            }
                        }
                        this.blogs = user_blogs
                        this.blogs.forEach((blog) => {
                            blog.image_url = blog.image_url.replace("static/", "")
                        });
                    })
                    .catch(error => {
                        console.log(error);
                    });
            },
            fetchUserBlogs(id) {
                console.log(id)
                for (let blog in this.blogs) {
                    if (blog.user_id == id) {
                        this.user_blogs.append(blog)
                    }
                }
                this.blogs = this.user_blogs
                console.log(user_blogs, blogs)



                // const response = fetch('http://127.0.0.1:8080/api/user/blogs', {
                //   headers: {
                //     "Content-type": "application/json",
                //     // "Authentication-Token":this.auth_token
                //   },
                //   method: "GET",
                // }).then((response) => response.json())
                //   .then(response => {
                //     this.blogs = response.user_blogs;
                //   })
                //   .catch(error => {
                //     console.log(error);
                //   });

            },
            editBlog(blog) {
                // Get the edited values from the form fields
                const updatedBlog = {
                    title: document.querySelector('#title').value,
                    caption: document.querySelector('#caption').value,
                    image_url: document.querySelector('#image_url').value
                };
                blog.title = updatedBlog.title
                blog.caption = updatedBlog.caption
                blog.image_url = updatedBlog.image_url

                // Send a PUT request to the server to update the blog
                response = fetch(`http://127.0.0.1:8080/api/blogs/${blog.id}/put`, {
                    headers: {
                        'Content-Type': 'application/json',
                        "Authentication-Token": this.auth_token,
                    },
                    method: 'PUT',
                    body: JSON.stringify(updatedBlog)
                }).then(response => response.json())
                    .then(data => {
                        // Display a success message
                        this.$toast.success(data.message);
                        this.fetchBlogs();
                    })
                    .catch(error => {
                        // Display an error message
                        this.$toast.error(error.message);
                    });
            }
            ,
            deleteBlog(blog) {
                if (confirm("Are you sure you want to delete this blog?")) {
                    const response = fetch(`http://127.0.0.1:8080/api/blogs/${blog.id}/delete`, {
                        headers: {
                            "Content-type": "application/json",
                            "Authentication-Token": this.auth_token
                        },
                        method: "DELETE",
                    }).then(response => {
                        this.blogs = this.blogs.filter(b => b.id !== blog.id);
                        this.$toast.success(response.data.message);
                        this.fetchBlogs();
                    })
                        .catch(error => {
                            this.$toast.error(error.response.data.message);
                        });
                }
            },
            async exportBlogs() {
                // Call the API to export the blogs as CSV
                const response = await fetch('http://127.0.0.1:8080/api/export-csv', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.blogs),
                });
                const data = await response.json();

                // Show a notification once the export is done
                alert(data.message);
            },

        }
    })

var blogs = new Vue({
    el: '#blogs',
    data: {
        blogs: [],
    }
});
