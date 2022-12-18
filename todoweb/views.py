from django.shortcuts import render,redirect

from django.views.generic import View,TemplateView,CreateView,FormView,ListView,DetailView

from todoweb.forms import UserRegistrationForm,LoginForm,TodoForm
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator


from django.contrib.auth import authenticate,login,logout


from TODO.models import Todos


from django.contrib import messages


from django.urls import reverse_lazy
# Create your views here.


def signin_required(fn):
    def wrapper(request,*args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"you must login first")
            return redirect("signin")
        else:
            return fn(request,*args, **kwargs)
    return wrapper    






class RegisterView(CreateView):
    model =User 
    template_name="register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy("signin")


    # def get(self,request,*args,**kwargs):
    #     form=UserRegistrationForm()
    #     return render(request,"register.html",{"form":form})





    # def post(self,request,*args, **kwargs):
    #     form=UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         User.objects.create_user(**form.cleaned_data)
    #         return redirect("signup")
    #     else:
    #         print("error")
    #         return render(request,"register.html",{form:form})    



class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm
    # def get(self,request,*args, **kwargs):
    #     form=LoginForm()
    #     return render(request,"login.html",{"form":form})



    def post(self,request,*args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password") 
            print(uname,pwd)
            usr=authenticate(request,username=uname,password=pwd)

            
           
        if usr:
            login(request,usr)
            return redirect("home")
        else:
            print("invalid")
            return redirect("signin")  

class IndexView(TemplateView):
    template_name="index.html"
    # def get(self,request,*args, **kwargs):
    #     return render(request,"index.html")


@method_decorator(signin_required,name="dispatch")
class TodoListView(ListView):
    template_name="Todos-list.html"
    model=Todos
    context_object_name="todos"
    
    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)




       

    
    # def get(self,request,*args, **kwargs):
    #     qs=Todos.objects.filter(user=request.user)
    #     return render(request,"todos-list.html",{"todos":qs})

@method_decorator(signin_required,name="dispatch")
class TodoCreateView(CreateView):
    model=Todos
    form_class=TodoForm
    template_name="todo-add.html"
    success_url=reverse_lazy("todo-list")


    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)

      

    # def get(self,request,*args, **kwargs):
    #     form=TodoForm()
    #     messages.success(request,"your account has been created")
    #     return render(request,"todo-add.html",{"form":form})

    # def post(self,request,*args, **kwargs):
    #     form=TodoForm(request.POST)
    #     if form.is_valid():
    #         isinstance= form.save(commit=False)
    #         isinstance.user=request.user
    #         isinstance.save()

    #         return redirect("todo-list")
    #     else:
    #         return render(request,"todo-add.html",{"form":form})    

@method_decorator(signin_required,name="dispatch")
class TodoDetailView(DetailView):
    template_name="todo-detail.html"
    model=Todos
    context_object_name="todos"
    pk_url_kwarg="id"
    # def get(self,request,*args, **kwargs):
    #     id=kwargs.get("id")
    #     qs=Todos.objects.get(id=id)
    #     return render(request,"todo-detail.html",{"todo":qs})


def todo_delete_view(request,*args, **kwargs):
    id=kwargs.get("id")
    Todos.objects.get(id=id).delete()
    return redirect("todo-list")



@signin_required
def sign_out_view(request,*args, **kwargs):
    logout(request)
    return redirect("signin")
 