Vue.component('blogs', {
    template: `
        <div>
            <div v-for="blog in blogs" :key="blog.id" class="card">
            <h3>{{ blog.title }}</h3>
            <img v-bind:src="blog.image_url" class="card-img-top" alt="{{ blog.title }}" width="300" height="auto">
            <p class="card-text">{{ blog.caption }}</p>
            <p>By {{ blog.user.username }} on {{ blog.updated_at }}</p>
            <button @click="editBlog(blog.id)" class="btn btn-primary">Edit</button>
            <button @click="deleteBlog(blog.id)" class="btn btn-danger">Delete</button>
            </div>
        </div>
    `,
    data() {
        return {
            blogs: []
        };
    },
    mounted() {
        this.fetchBlogs();
    },
    methods: {
        fetchBlogs() {
            const response = fetch('http://127.0.0.1:8080/api/blogs', {
                headers: {
                    "Content-type": "application/json",
                    // "Authentication-Token":this.auth_token
                },
                method: "GET",
            }).then((response) => response.json())
                .then(response => {
                    this.blogs = response.blogs;
                })
                .catch(error => {
                    console.log(error);
                });
        },
        editBlog(id) {
            // TODO: implement edit blog functionality
        },
        deleteBlog(id) {
            // TODO: implement delete blog functionality
        }
    }
}
)

var blogs = new Vue({
    el: '#blogs',
    data: {
        blogs: [],
    }
});
