import os
from datetime import datetime
# 1. 导入所需模块
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.utils import secure_filename
# 导入 Flask-WTF 表单类
from forms import ContactForm
# 导入 SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# 2. 创建Flask应用实例
app = Flask(__name__)

# ★★★ 必须设置 Secret Key 才能使用 Session ★★★
# 在实际项目中，这应该是一个复杂、随机的字符串
app.secret_key = 'a_super_random_and_secret_string_12345!'

# 2. 配置上传文件夹的路径
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 数据库配置
# 设置数据库文件的路径，放在项目根目录下
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'messages.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭不需要的警告

# 创建数据库实例
db = SQLAlchemy(app)

# 定义联系消息的数据库模型
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键，自动递增
    name = db.Column(db.String(80), nullable=False)  # 名字，不能为空
    email = db.Column(db.String(120), nullable=False)  # 邮箱，不能为空
    message = db.Column(db.Text, nullable=False)  # 消息内容，不能为空
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间，默认为当前时间

    def __repr__(self):
        return f'<Contact {self.name}>'

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 3. 定义路由和视图函数

# 1. 首页：根据 Session 判断登录状态
@app.route('/')
def home():
    # 检查 session 字典中是否有 'username' 这个键
    if 'username' in session:
        # 如果有，说明用户已登录
        username = session['username']
        return render_template('index.html', username=username)
    else:
        # 如果没有，说明是游客
        return render_template('index.html')

# "关于我"页面路由：当用户访问 /about 时
@app.route('/about')
def about():
    # 渲染 templates/about.html 文件
    return render_template('about.html')

# 动态路由示例：可以展示不同用户的个人资料
@app.route('/user/<username>')
def show_user_profile(username):
    # 将从URL中获取的 username 传递给HTML模板
    return render_template('user_profile.html', name=username)

# ===== 表单处理示例：登录功能 =====

# 2. 登录页：验证成功后，在 Session 中记录用户名
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_from_form = request.form['username']
        password_from_form = request.form['password']

        # 简单的登录逻辑判断
        if username_from_form == 'admin' and password_from_form == '123456':
            # 管理员登录成功！把用户名存入 session 字典
            session['username'] = username_from_form
            session['user_role'] = 'admin'
            # 在重定向前，闪现一条成功的消息
            flash(f'🎉 欢迎，{username_from_form}！您已成功登录为管理员。', 'success')
            return redirect(url_for('home'))
        elif password_from_form == 'guest':
            # 访客登录成功！
            session['username'] = username_from_form
            session['user_role'] = 'guest'
            # 在重定向前，闪现一条成功的消息
            flash(f'👋 欢迎，{username_from_form}！您已成功登录为访客。', 'success')
            return redirect(url_for('home'))
        else:
            # 登录失败，闪现错误消息
            flash('❌ 用户名或密码错误！请重试。', 'error')
            # 重定向到登录页面而不是失败页面，让用户看到错误消息
            return redirect(url_for('login'))
    # 如果是 GET 请求，显示登录页面
    return render_template('login.html')

# 登录失败页面
@app.route('/login_failed/<username>')
def login_failed(username):
    return render_template('login_failed.html', username=username)

# 3. 注销页：从 Session 中移除用户名
@app.route('/logout')
def logout():
    # 获取当前用户名用于显示消息
    current_username = session.get('username', '用户')

    # 使用 .pop() 方法从 session 字典中移除 'username'
    session.pop('username', None)
    session.pop('user_role', None)

    # 在重定向前，闪现一条注销成功的消息
    flash(f'👋 {current_username}，您已成功注销。期待您的下次访问！', 'info')
    # 重定向回首页
    return redirect(url_for('home'))

# ===== URL 构建和重定向示例 =====

# 管理员的欢迎页面
@app.route('/admin')
def hello_admin():
    return render_template('admin.html')

# 访客的欢迎页面
@app.route('/guest/<guest>')
def hello_guest(guest):
    return render_template('guest.html', guest_name=guest)

# 这是我们的逻辑判断入口
# 它会根据 URL 中的 <name> 决定跳转到哪里
@app.route('/profile/<name>')
def user_profile(name):
    # 如果名字是 'admin'
    if name == 'admin':
        # 就重定向到 hello_admin 这个函数对应的 URL
        # url_for('hello_admin') 会生成 '/admin'
        return redirect(url_for('hello_admin'))
    else:
        # 否则，就重定向到 hello_guest 函数对应的 URL
        # 我们需要给 hello_guest 传递 guest 参数，所以是 url_for('hello_guest', guest=name)
        # 这会生成类似 '/guest/张三' 这样的 URL
        return redirect(url_for('hello_guest', guest=name))

# ===== 文件上传功能 =====

# 3. 创建文件上传的路由
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 4. 检查请求中是否包含文件部分
        if 'file_to_upload' not in request.files:
            flash('请求中没有文件部分', 'error')
            return redirect(request.url)

        file = request.files['file_to_upload']

        # 5. 如果用户没有选择文件，浏览器也会提交一个没有文件名的空部分
        if file.filename == '':
            flash('没有选择文件', 'info')
            return redirect(request.url)

        # 6. 检查文件是否被允许
        if file and allowed_file(file.filename):
            # 7. 使用 secure_filename 清理文件名，确保安全
            filename = secure_filename(file.filename)

            # 8. 将文件保存到我们配置的上传文件夹中
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            flash(f'📁 文件 "{filename}" 上传成功! 文件已保存到 uploads 文件夹中。', 'success')
            return redirect(url_for('upload_file'))
        else:
            flash('❌ 不允许的文件类型！请上传支持的文件类型：txt, pdf, png, jpg, jpeg, gif, doc, docx, xls, xlsx', 'error')
            return redirect(request.url)

    # 如果是 GET 请求，或者上传失败后，都显示上传页面
    return render_template('upload.html')

# Flask-WTF 联系表单路由
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # 实例化我们的表单类
    form = ContactForm()

    # 使用 form.validate_on_submit() 来处理表单提交和验证
    # 这个方法会自动检查请求是否为 POST 并且所有验证器都通过
    if form.validate_on_submit():
        # 如果验证通过，通过 .data 属性获取数据
        name = form.name.data
        email = form.email.data
        message = form.message.data

        # 创建新的Contact记录并保存到数据库
        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()

        print(f"收到来自 {name} ({email}) 的消息: {message}")
        print(f"消息已保存到数据库，ID: {new_contact.id}")

        flash(f'🎉 感谢您的消息，{name}！我们已收到并保存到数据库中。', 'success')
        return redirect(url_for('contact'))

    # 如果是 GET 请求或验证失败，则渲染模板
    # 如果验证失败，WTForms 会自动向 form 对象添加错误消息
    return render_template('contact.html', form=form)

# 消息列表页面路由
@app.route('/messages')
def messages():
    # 从数据库中获取所有联系消息，按创建时间倒序排列
    all_messages = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('messages.html', messages=all_messages)

# AJAX演示页面路由
@app.route('/ajax-demo')
def ajax_demo():
    return render_template('ajax_demo.html')

# AJAX处理路由 - say_hello
@app.route('/ajax/say-hello', methods=['POST'])
def ajax_say_hello():
    # 获取前端发送的数据
    data = request.get_json()
    name = data.get('name', '朋友')
    lastname = data.get('lastname', '')

    # 返回JSON响应
    return jsonify({
        'success': True,
        'message': f'Hello from {name} {lastname}!',
        'action': 'turn_green'
    })

# AJAX处理路由 - say_goodbye
@app.route('/ajax/say-goodbye', methods=['POST'])
def ajax_say_goodbye():
    # 返回JSON响应
    return jsonify({
        'success': True,
        'message': 'Goodbye, whoever you are!',
        'action': 'turn_red'
    })

# 4. 启动应用
if __name__ == '__main__':
    # 在应用启动前创建数据库表
    with app.app_context():
        db.create_all()
        print('数据库和表创建成功！')
        print('数据库文件位置:', app.config['SQLALCHEMY_DATABASE_URI'])

    # debug=True 开启调试模式，代码修改后服务器会自动重启
    # port=9250 指定一个在你范围内的端口
    # host='0.0.0.0' 允许其他计算机访问此应用
    app.run(debug=True, host='0.0.0.0', port=9250)