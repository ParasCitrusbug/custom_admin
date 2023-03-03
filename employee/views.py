import logging

from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views import View

from employee import forms
from .models import EmployeeData, UserData
from .middleware.auth_middleware import SessionMiddleware

# Get an instance of a logger
logger = logging.getLogger(__name__)


class LoginUser(CreateView):
    """login user"""

    form_class = forms.UserForm
    template_name = "employees/login.html"

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        form_data = self.form_class(request.POST)
        user = UserData.objects.filter(email=email)
        if user and form_data:
            user = UserData.objects.get(email=email)
            if check_password(password, user.password):
                request.session["email"] = email
                return redirect("home")
            else:
                messages.error(request, "invalid password")
                return redirect("login")
        else:
            messages.error(request, "invalid email and password")
            return redirect("login")


class EmployeeHome(TemplateView):
    """view of employee data"""

    template_name = "employees/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee_data = EmployeeData.objects.all()
        context["employee_data"] = employee_data
        return context

    @method_decorator(SessionMiddleware, name="dispatch")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AddEmployee(View):
    """Employee data add"""

    template_name = "employees/add_employee.html"
    employee_form = forms.EmployeeForm()

    @method_decorator(SessionMiddleware, name="dispatch")
    def get(self, request):
        return render(request, self.template_name)

    @method_decorator(SessionMiddleware, name="dispatch")
    def post(self, request):
        try:
            name = request.POST.get("name")
            employee_id = request.POST.get("employee_id")
            phone_number = request.POST.get("phone_number")
            address = request.POST.get("address")
            working = request.POST.get("working")
            department = request.POST.get("department")
            working = False if working is None else True
            EmployeeData.objects.create(
                name=name,
                employee_id=employee_id,
                phone_number=phone_number,
                address=address,
                working=working,
                department=department,
            )
            return redirect("home")
        except Exception as e:
            messages.info(request, e)
            return redirect("add_employee")


class DeleteEmployee(View):
    """delete data of employee"""

    @method_decorator(SessionMiddleware, name="dispatch")
    def get(self, request, id):

        employee_object = EmployeeData.objects.get(pk=id)
        employee_object.delete()
        return redirect("home")


class UpdateEmployee(View):
    """redirect to only update data of employee"""

    template_name = "employees/update_employee.html"

    @method_decorator(SessionMiddleware, name="dispatch")
    def get(self, request, id):

        employee_object = EmployeeData.objects.get(pk=id)
        context = {"emp": employee_object}
        return render(request, self.template_name, context)

    @method_decorator(SessionMiddleware, name="dispatch")
    def post(self, request, pk):
        try:
            name = request.POST.get("name")
            employee_id = request.POST.get("employee_id")
            phone_number = request.POST.get("phone_number")
            address = request.POST.get("address")
            working = request.POST.get("working")
            department = request.POST.get("department")
            working = False if working is None else True

            EmployeeData.objects.filter(pk=pk).update(
                name=name,
                employee_id=employee_id,
                phone_number=phone_number,
                address=address,
                working=working,
                department=department,
            )
            return redirect("home")
        except Exception as e:
            messages.info(request, e)
            return redirect("update_employee", pk)


class LogoutUser(View):
    """Logout Password"""

    def get(self, request):
        try:
            del request.session["email"]
        except KeyError:
            print("error")
        return redirect("login")


class ForgotPassword(CreateView):
    """Forgot Password"""

    form_class = forms.ForgotPasswordForm
    template_name = "employees/forgot_password.html"

    def post(self, request):
        email = request.POST.get("email")
        user_form_field = self.form_class(request.POST)
        user = UserData.objects.filter(email=email)

        if user and user_form_field:
            Employee_object = UserData.objects.get(email=email)
            messages.info(request, "send email to you")
            return redirect(f"/employee/change_password/{Employee_object.id}")
        else:
            messages.info(request, "email is not register")
            return redirect("forgot_password")


class ChangePassword(View):
    """Change password"""

    template_name = "employees/change_password.html"

    def get(self, request, id):
        change_password_form = forms.ChangePasswordForm()
        context = {"form": change_password_form, "id": id}
        return render(request, self.template_name, context)

    def post(self, request, id):
        user_id = UserData.objects.get(pk=id)
        password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "confirm password is not match")
            return redirect(f"/employee/change_password/{id}")
        user_id.password = password
        user_id.save()
        return redirect("login")
