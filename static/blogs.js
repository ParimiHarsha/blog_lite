Vue.component('blogs',
  {
    template: `
    <div>
    <div v-for="blog in blogs" :key="blog.id" class="card">
      <h3>{{ blog.title }}</h3>
      <img v-bind:src="blog.image_url" class="card-img-top" alt="{{ blog.title }}">
      <p class="card-text">{{ blog.caption }}</p>
      <p>By {{ blog.user.username }} on {{ blog.updated_at }}</p>
  
      <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#blogModal">
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
      <button @click="deleteBlog(blog)" class="btn btn-danger">Delete</button>
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
      // this.editBlog = this.editBlog.bind(this);
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
            'Content-Type': 'application/json'
          },
          method: 'PUT',
          body: JSON.stringify(updatedBlog)
        }).then(response => response.json())
          .then(data => {
            // Update the blog in the blogs array
            // const index = this.blogs.findIndex(b => b.id === blog.id);
            // if (index >= 0) {
            //   this.blogs[index] = data.blog;
            // }
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
              // "Authentication-Token":this.auth_token
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
    },
  }
)

var blogs = new Vue({
  el: '#blogs',
  data: {
    blogs: [],
  }
});
