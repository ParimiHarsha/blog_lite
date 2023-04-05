// Search bar component that allows users to search for other users
const SearchBar = {
    props: {
      // Function to call when the user submits the search query
      onSubmit: {
        type: Function,
        required: true
      }
    },
    data() {
      return {
        // The search query entered by the user
        query: ''
      };
    },
    methods: {
      // Function to call when the user submits the search query
      submit() {
        // Call the onSubmit function passed in as a prop, passing it the search query
        this.onSubmit(this.query);
        // Reset the search query
        this.query = '';
      }
    },
    template: `
      <div class="search-bar">
        <input v-model="query" type="text" placeholder="Search users...">
        <button @click="submit">Search</button>
      </div>
    `
  };
  
  // User card component that displays information about a user
  const UserCard = {
    props: {
      // The user to display information about
      user: {
        type: Object,
        required: true
      },
      // Function to call when the user clicks the "Follow" button
      onFollow: {
        type: Function,
        required: true
      },
      // Function to call when the user clicks the "Unfollow" button
      onUnfollow: {
        type: Function,
        required: true
      }
    },
    methods: {
      // Function to call when the user clicks the "Follow" button
      follow() {
        // Call the onFollow function passed in as a prop, passing it the user ID
        this.onFollow(this.user.id);
      },
      // Function to call when the user clicks the "Unfollow" button
      unfollow() {
        // Call the onUnfollow function passed in as a prop, passing it the user ID
        this.onUnfollow(this.user.id);
      }
    },
    template: `
      <div class="user-card">
        <img :src="user.avatar" alt="User avatar">
        <div class="user-info">
          <h2>{{ user.name }}</h2>
          <p>{{ user.bio }}</p>
        </div>
        <div class="user-actions">
          <!-- Display "Follow" button if user is not followed -->
          <button v-if="!user.followed" @click="follow">Follow</button>
          <!-- Display "Unfollow" button if user is followed -->
          <button v-if="user.followed" @click="unfollow">Unfollow</button>
        </div>
      </div>
    `
  };
  
  // User list component that displays a list of UserCard components for each user in the list
  const UserList = {
    props: {
      // The list of users to display
      users: {
        type: Array,
        required: true
      },
      // Function to call when the user clicks the "Follow" button for a user
      onFollow: {
        type: Function,
        required: true
      },
      // Function to call when the user clicks the "Unfollow" button for a user
      onUnfollow: {
        type: Function,
        required: true
      }
    },
    components: {
      // Use the UserCard component to display information about each user
      UserCard
    },
    template: `
      <div class="user-list">
        <UserCard v-for="user in users" :key="user.id" :user="user" :onFollow="onFollow" :on`
  }
  