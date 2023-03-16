Vue.component('message-board', {
    data: {
        visitor_name: '',
        visitor_message: '',
        message: '',
    },
});

var app = new Vue({
    el: '#app',
    data: {
        message: 'hel world',
    },
    methods: {
        hey() {
            console.log(this.message);
            this.message = 'Hi';
        },
    },
});
