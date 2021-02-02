from flask import Flask, render_template, request, url_for,redirect


app = Flask(__name__)

posts = {
    0:{
        'title': 'Hello, World',
        'content': 'This is my first blog post!'
    }
}

@app.route('/')
def home():
    return render_template('home.jinja2', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = posts.get(post_id)
    if not post:    # post will not be None if not found; not None => True
        return render_template('404.jinja2', message=f'A post with id {post_id} was not found.')
    return render_template('post.jinja2',post=post)

@app.route('/post/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        title = request.args.get('title')
        content = request.args.get('content')
        post_id = len(posts)
        posts[post_id] = {'id': post_id, 'title': title, 'content': content}
        return redirect(url_for('post',post_id=post_id)) # url_for takes a function name as an argument.
    return render_template('create.jinja2')

if __name__ == '__main__':
    app.run(debug=True)

