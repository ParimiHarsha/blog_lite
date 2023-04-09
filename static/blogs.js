Vue.component('blogs',
  {
    template: `
    <div class='col-6 text-center'>
    <div v-for="blog in blogs" :key="blog.id" class="card">
      <h3>{{ blog.title }}</h3>
      <img v-bind:src="blog.image_url" class="card-img-top" alt="{{ blog.title }}">
      <p class="card-text">{{ blog.caption }}</p>
      <p>By {{ blog.user.username }} on {{ blog.updated_at }}</p>
  
      <button v-if="blog.user.id == user_id" type="button" class="btn btn-primary btn sm" data-toggle="modal" data-target="#blogModal">
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
      <button  v-if="blog.user.id == user_id" @click="deleteBlog(blog)" class="btn btn-danger btn sm">Delete</button>
      </div>
  </div>
    `,
    data: (instance) => ({

      blogs: [],
      user_blogs: [],
      auth_token: temp,
      userPage: instance.userPage || false,
      userId: instance.userId || null,
    }),
    props: {
      user_id: {}
    },
    mounted() {
      this.getCurrentUser()
        .then((user) => {
          this.currentUser = user;
          this.fetchBlogs(user.id);
        });
      console.log(this.userPage, this.userId)
      if (this.userPage) {
        this.fetchUserBlogs(this.userId);
      }
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
            this.blogs = response.blogs;
            console.log(this.userPage, this.userId);
          })
          .catch(error => {
            console.log(error);
          });
      },
      fetchUserBlogs(id) {
        // var user_blogs = [];
        console.log(id)
        for (let blog in this.blogs) {
          if (blog.user_id == id) {
            this.user_blogs.append(blog)
          }
        }
        this.blogs = this.user_blogs
        console.log(user_blogs, blogs)
      },
      editBlog(blog) {
        // Get the edited values from the form fields
        const updatedBlog = {
          title: document.querySelector('#title').value,
          caption: document.querySelector('#caption').value,
          image_url: document.querySelector('#image_url').value,
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
    },
    watch: {
      $route(to, from) {
        if (this.userPage) {
          this.fetchUserBlogs(this.userId);
          console.log(this.userPage)
        }
      },
      userPage(newValue, oldValue) {
        if (newValue && this.userId) {
          this.fetchUserBlogs(this.userId);
        } else {
          this.blogs = []; // clear user_blogs when navigating away from a user page
        }
      },
      // userId(newValue, oldValue) {
      //   if (this.userPage && newValue) {
      //     this.fetchUserBlogs(newValue);
      //   } else {
      //     this.blogs = []; // clear user_blogs when navigating away from a user page
      //   }
      // }
    }
  }
)

var blogs = new Vue({
  el: '#blogs',
  data: {
    blogs: [],
  }
});
