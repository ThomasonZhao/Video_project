## 第二天 用户注册与登陆功能

### 创建users应用
在Django中，应用于应用之间分模块化处理，每一个应用各司其职，
一个应用只提供一种功能，比如users应用只提供用户相关功能，
comment应用只提供评论相关功能，这能提高代码的重复利用率。  
在django中，只需要下面一条命令，即可建立users应用
```
python3 manage.py startapp users
```
在创建完成后，我们需要立即到`videoproject/settings.py`中注册应用，
不然是无法调用这个应用的哦
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
]
```
创建users应用之后我们肯定在网页中会使用到这个应用，
所以我们需要在`videoproject/urls.py`中分发路由
```
# videoproject/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]
```

### 需求分析
在Django应用中，最先编辑的应该是models.py文件，
因为这个文件定义整个应用的数据结构。
因此，我们来对将要开展的用户注册与登陆功能进行需求分析。  
Django作为一个Web开发框架，自带了简单的用户注册与登陆功能，其自带字段如下: 
+ username
+ password
+ last_login
+ is_superuser
+ first_name
+ last_name
+ email
+ is_staff
+ is_active
+ date_joined  

但一般来说，一个视频网站还应该有一些更加个性化的需求，所以我们需要自定义一些字段：
+ nickname（昵称）
+ avatar（头像）
+ mobile（手机号码）
+ gender（性别）
+ subscribe（是否订阅）

因此，在后面的建表中我们需要手动创建这些字段。

### 建表
在分析完users的需求之后，我们就可以开始建表了，
只需要在`users/models.py`里面写入代码：
```
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女')
    )
    nickname = models.CharField(blank=True, null=True, max_length=20)
    avatar = models.FileField(upload_to='avtar/')
    mobile = models.CharField(blank=True, null=True, max_length=13)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    subscribe = models.BooleanField(default=False)

    class Meta:
        db_table = "v_user"
```

### urls分发路由
我们前面在创建users应用中已经为这个应用添加了路由，
现在我们需要为应用里面的功能添加所需路由。  
在user文件夹下面，新建urls.py文件，写入登录、注册和退出的url信息。
app_name是命名空间，我们命名为'users'。
```
from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
]
```

### 视图函数
url路由配置好了，我们下面就开始写视图函数代码了。 

#### 注册函数
我们先来写注册函数，写注册，当然得有注册表单了，幸运的是，在django中，可以用代码来生成表单。
我们只需在users下新建forms.py文件，然后写入注册表单的代码。
```
class SignUpForm(UserCreationForm):
    username = forms.CharField(min_length=4, max_length=30,
                               error_messages={
                                   'min_length': '用户名不能少于4个字符',
                                   'max_length': '用户名不能大于30个字符',
                                   'required': '用户名不能为空',
                               },
                               widget=forms.TextInput(attrs={'placeholder': '请输入用户名'}))
    password1 = forms.CharField(min_length=8, max_length=30,
                                error_messages={
                                    'min_length': '密码不能小于8个字符',
                                    'max_length': '密码不能大于30个字符',
                                    'required': '密码不能为空',
                                },
                                widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}))
    password2 = forms.CharField(min_length=8, max_length=30,
                                error_messages={
                                    'min_length': '密码不能小于8个字符',
                                    'max_length': '密码不能大于30个字符',
                                    'required': '密码不能为空',
                                },
                                widget=forms.PasswordInput(attrs={'placeholder': '请确认密码'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    error_messages = {'password_mismatch': '两次密码不一致'}
```
我们的表单一共有三个字段：username、password1、password2，它们都是CharField类型，widget分别是TextInput和PasswordInput。
而且django是自带验证的，只需要我们配置好error_messages字典，当form验证的时候，就会显示我们自定义的错误信息。  
有了注册表单后，就可以在前端模板和视图函数`users/views.py`中使用它。
```
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password1 = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password1)
            auth_login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

```
在signup函数中，我们通过form = SignUpForm初始化一个表单，并在render函数中传递给模板。  
注册模板文件写在了`templates/registration/signup.html`中。
由于本人不太会写前端的交互代码，前端开发设计交给了RyanMa。在此阶段就先直接复制了 [原项目](https://github.com/geeeeeeeek/videoproject)
的前端代码，在RyanMa开发设计完成后会逐步替换前端交互界面。  
前端最核心的代码莫过于是表单的提交了，其他的都是交互和排版，这边就只展示form有关代码
```
<form class="ui large form" novalidate method="post" action="{% url 'users:signup' %}" enctype="multipart/form-data" >
            {% csrf_token %}
            <div class="ui stacked segment">
                <div class="field">
                    <div class="ui left icon input">
                        <i class="user icon"></i>
                        {{form.username}}
                    </div>
                </div>
                <div class="field">
                    <div class="ui left icon input">
                        <i class="lock icon"></i>
                        {{form.password1}}
                    </div>
                </div>
                <div class="field">
                    <div class="ui left icon input">
                        <i class="lock icon"></i>
                        {{form.password2}}
                    </div>
                </div>
                <button class="ui fluid large teal submit button" type="submit">注册</button>
            </div>
            {% include "base/form_errors.html" %}
        </form>
```
这个form表单会把数据通过POST请求传递给view.py里面的signup注册函数，
在signup注册函数中，通过如下四行代码来实现自动注册的。
```
username = form.cleaned_data.get('username')
            raw_password1 = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password1)
            auth_login(request, user)
```

####登陆函数
登陆函数和注册函数同理，只需要略微更改一些细节上的参数，这里就不多赘述了。  
只是重点讲一下登陆函数中一个重要的参数：next
```
def login(request):
    if request.method == 'POST':
        next = request.POST.get('next', '/')
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect(next)
        else:
            print(form.errors)
    else:
        next = request.GET.get('next', '/')
        form = UserLoginForm()
    print(next)
    return render(request, 'registration/login.html', {'form': form, 'next':next})
```
从上面的代码中不难看出，登陆函数会多一个参数next。next对应的是登录后要跳转的url，
其实这是一种场景，假如你在购物网站买东西，最后付款的时候，会跳转到付款页，
假如你没有登录，网站会提示你登录，登录后，会再次跳转到付款页的这样一个反复横跳的工具。  
当然了，跳转到登录页的时候，需要你在url后追加next参数，
如  aaa. com/login/?next=bbb. com这样用户登录后就会跳到bbb. com

####退出函数
退出函数异常地简单，只需要一句自带的`auth_logout(request)`就可以了：
```
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('home')
```
