Vue.component('search-bar', {
    template: `
      <div>
        <input v-model="searchTerm" type="text" placeholder="Search for users...">
        <ul>
          <li v-for="user in searchResults" :key="user.id">
            <div>{{ user.username }}</div>
            <button v-if="!user.is_followed" @click="follow(user)">Follow</button>
            <button v-if="user.is_followed" @click="unfollow(user)">Unfollow</button>
            <button @click="viewProfile(user)">View Profile</button>
          </li>
        </ul>
      </div>
    `,
    data() {
        return {
            searchTerm: '',
            searchResults: [],
        };
    },
    methods: {
        searchUsers() {
            // Send a GET request to the server with the search term
            // and update the searchResults array with the results
            const response = fetch(`http://127.0.0.1:8080/api/search?search=${encodeURIComponent(this.searchTerm)}`, {
                headers: {
                    "Content-type": "application/json",
                    // "Authentication-Token":this.auth_token
                },
                method: "GET",
            }).then((response) => response.json())
                .then((data) => {
                    this.searchResults = data.users;
                })
                .catch((error) => {
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
                    // "Authentication-Token":this.auth_token
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
                    // "Authentication-Token":this.auth_token
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