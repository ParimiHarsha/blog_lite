Vue.component('search-bar', {
    template: `
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-8 offset-md-2">
            <div class="input-group mb-3">
                <input v-model="searchTerm" type="text" class="form-control" placeholder="Search for users...">
                <div class="input-group-append">
                <button class="btn btn-primary" type="button">Search</button>
                </div>
            </div>
            <ul class="list-group">
                <li v-for="user in searchResults" :key="user.id"
                class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                    <h5>{{ user.username }}</h5>
                </div>
                <div>
                    <button v-if="!user.is_followed" class="btn btn-primary" @click="follow(user)">Follow</button>
                    <button v-if="user.is_followed" class="btn btn-secondary" @click="unfollow(user)">Unfollow</button>
                    <a :href="'/user_profile/'+ user.id">View Profile</a>
                </div>
                </li>
            </ul>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            searchTerm: '',
            searchResults: [],
            auth_token: temp,
        };
    },
    methods: {
        searchUsers() {
            // Send a GET request to the server with the search term
            // and update the searchResults array with the results
            const response = fetch(`http://127.0.0.1:8080/api/search?search=${encodeURIComponent(this.searchTerm)}`, {
                headers: {
                    "Content-type": "application/json",
                    "Authentication-Token": this.auth_token
                },
                method: "GET",
            }).then((response) => response.json())
                .then((data) => {
                    this.searchResults = data.users;
                })
                .catch((error) => {
                    console.log(this.auth_token)
                    console.log(error);
                });
        },
        viewProfile(user) {
            // Navigate to the user's profile page
            this.$router.push('/users/' + user.id);
        },
        follow(user) {
            // Send a POST request to the server to follow the user
            const response = fetch('http://127.0.0.1:8080/api/users/' + user.id + '/follow', {
                headers: {
                    "Content-type": "application/json",
                    "Authentication-Token": this.auth_token
                },
                method: "POST",
            })
                .then((response) => {
                    if (response.ok) {
                        return response;
                    } else {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                })
                .then((data) => {
                    data.user.followed = true;
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        unfollow(user) {
            // Send a POST request to the server to unfollow the user
            const response = fetch('http://127.0.0.1:8080/api/users/' + user.id + '/unfollow', {
                headers: {
                    "Content-type": "application/json",
                    "Authentication-Token": this.auth_token
                },
                method: "POST",
            })
                .then((response) => {
                    user.followed = false;
                })
                .catch((error) => {
                    console.log(error);
                });
        },
    },
    watch: {
        searchTerm() {
            this.searchUsers();
        },
    },
});

var app = new Vue({
    el: '#app',
    data: {
        searchTerm: '',
        searchResults: [],
    }
});