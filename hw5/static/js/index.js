// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        post_mode: false,
        post_content: "",
        posts: [],
        add_email: ""
        // Complete as you see fit.
    };

    app.set_mode = function(new_status){
        app.vue.post_mode = new_status;
    };

    app.add_post = function(){
        axios.post(add_post_url,
            {
                post_content: app.vue.post_content,
                add_email: app.vue.add_email,
            })
            .then(function (response){
                app.vue.posts.push({
                    id: response.data.id,
                    name: response.data.name,
                    email: response.data.email,
                    post_content: app.vue.post_content,
                    likers: "",
                    haters: "",
                    rating: 0,
                });
                app.enumerate(app.vue.posts);
                app.reset_post();
                app.set_mode(false);
            });
    };

    app.reset_post = function (){
        app.vue.post_content = "";
    };

    app.set_rating = (post_idx, value) => {
        let post = app.vue.posts[post_idx];
        Vue.set(post, 'rating', value);
        axios.post(set_rating_url, {post_id: post.id, rating: value});
    };

    app.show_likers = (post_idx, value) => {
        let post = app.vue.posts[post_idx];
        Vue.set(post, 'show_likers', value);
        axios.post(show_likers_url, {post_id: post.id}).then((result) => {
            post.likers = result.data.likers;
        });
    };

    app.show_haters = (post_idx, value) => {
        let post = app.vue.posts[post_idx];
        Vue.set(post, 'show_haters', value);
        axios.post(show_haters_url, {post_id: post.id}).then((result) => {
            post.haters = result.data.haters;
        });
    };

    app.set_haters = (post_idx, value) => {
        let post = app.vue.posts[post_idx];
        Vue.set(post, 'rating', value);
        axios.post(set_rating_url, {post_id: post.id, rating: value});
    };

    app.set_likers = (post_idx) => {
        let post = app.vue.posts[post_idx];
        Vue.set(post, 'rating', value);
        axios.post(set_rating_url, {post_id: post.id, rating: value});
    };

    app.del_post = (post_idx) => {
        let id = app.vue.posts[post_idx].id;
        axios.get(del_post_url, {params: {id: id}}).then(function ( response){
            for (let i=0; i<app.vue.posts.length; i++){
                if(app.vue.posts[i],id == id){
                    app.vue.posts.reverse().splice(i, 1);
                    app.enumerate(app.vue.posts);
                    break;
                }
            }
        })
    }

    app.complete = (a) => {
        a.map((post) => {
            post.rating = 0;
            post.show_likers = false;
            post.show_haters = false;
            post.likers = "";
            post.haters = "";
        })
        return a;
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        set_mode: app.set_mode,
        add_post: app.add_post,
        reset_post: app.reset_post,
        set_rating: app.set_rating,
        show_likers: app.show_likers,
        show_haters: app.show_haters,
        set_haters: app.set_haters,
        set_likers: app.set_likers,
        del_post: app.del_post
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
        // Typically this is a server GET call to load the data.
        axios.get(load_posts_url)
            .then(function (response) {
                app.complete(response.data.posts);
                app.vue.posts = app.enumerate(response.data.posts);
                app.vue.add_email = response.data.email;
                })
            .then(() => {
                for (let post of app.vue.posts) {
                    axios.get(get_rating_url, {params: {"post_id": post.id}})
                    .then((result) => {
                        post.rating = result.data.rating;
                    });
                }
            });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
