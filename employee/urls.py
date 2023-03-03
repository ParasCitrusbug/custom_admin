from django.urls import path

from employee.views import (
    AddEmployee,
    ChangePassword,
    DeleteEmployee,
    EmployeeHome,
    ForgotPassword,
    LoginUser,
    LogoutUser,
    UpdateEmployee,
)

urlpatterns = [
    path("home/", EmployeeHome.as_view(), name="home"),
    path("add_employee/", AddEmployee.as_view(), name="add_employee"),
    path("delete_employee/<uuid:id>", DeleteEmployee.as_view(), name="delete_employee"),
    path("update_employee/<uuid:id>", UpdateEmployee.as_view(), name="update_employee"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", LogoutUser.as_view(), name="logout"),
    path("forgot_password/", ForgotPassword.as_view(), name="forgot_password"),
    path("change_password/<uuid:id>", ChangePassword.as_view(), name="change_password"),
]
