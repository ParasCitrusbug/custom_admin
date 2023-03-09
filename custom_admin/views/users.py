"""
This is a view module to define list, create, update, delete views.
You can define different view properties here.
"""
from django.contrib.auth import login
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    AuthenticationForm,
    PasswordResetForm,
)
from django.db.models import Q
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.http import JsonResponse
from custom_admin.forms import UserChangeForm, MyUserCreationForm
from custom_admin.mixins import HasPermissionsMixin
from django_datatables_too.mixins import DataTableMixin
from custom_admin.views.generic import (
    MyLoginRequiredView,
    MyUpdateView,
    MyListView,
    MyCreateView,
    MyDetailView,
    MyDeleteView,
)
from user.models import User
from employee.models import Employee


class IndexView(LoginRequiredMixin, TemplateView):
    """This for Total count of data user and employee"""

    template_name = "core/index.html"
    context = {}

    def get(self, request, *args, **kwargs):
        self.context["user_count"] = User.objects.all().exclude(is_staff=True).count()
        self.context["employee_count"] = Employee.objects.all().count()
        return render(request, self.template_name, self.context)


class UserDetailView(MyDetailView):
    """
    View for User details
    """

    model = User
    template_name = "core/adminuser/user_details.html"
    permission_required = ("core.view_user",)

    def get(self, request, pk):
        """Get User data"""

        context = {}
        user_data = User.objects.get(pk=pk)
        context["user_data"] = user_data
        return render(request, self.template_name, context)



class UserListView(MyListView):
    """
    View for User listing
    """

    ordering = ["id"]
    model = User
    queryset = model.objects.exclude(is_superuser=True)
    template_name = "core/adminuser/user_list.html"
    permission_required = ("core.view_user",)

    def get_queryset(self):
        """Override queryset to add extra functionality"""
        return self.model.objects.exclude(is_superuser=True).exclude(
            username=self.request.user
        )


class UserCreateView(MyCreateView):
    """
    View to create User
    """

    model = User
    form_class = MyUserCreationForm
    template_name = "core/adminuser/user_forms.html"
    permission_required = ("core.add_user",)

    def get_form_kwargs(self):
        """Get data from kwargs"""

        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class UserLoginView(LoginView):
    """
    View for user login activity.
    Inherited from Django Auth LoginView
    """

    form_class = AuthenticationForm
    template_name = "core/taste_dna/registration/login.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        if form.get_user().is_staff == True:
            login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        else:
            raise PermissionDenied


class UserUpdateView(MyUpdateView):
    """
    View to update User
    """

    model = User
    form_class = UserChangeForm
    template_name = "core/adminuser/user_forms.html"
    permission_required = ("core.change_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("user-list")


class UserPasswordView(MyUpdateView):
    """
    View to change User Password
    """

    model = User
    form_class = AdminPasswordChangeForm
    template_name = "core/adminuser/password_change_form.html"
    permission_required = ("core.change_user",)

    def get_form_kwargs(self):
        """Get data from kwargs"""

        kwargs = super().get_form_kwargs()
        # kwargs['user'] = self.request.user
        kwargs["user"] = kwargs.pop("instance")
        return kwargs


class UserPasswordResetView(PasswordResetView):
    """
    View for user reset password activity that sends mail to user with steps to rest.
    Inherited from Django Auth PasswordResetView
    """

    template_name = "core/taste_dna/password_reset.html"
    email_template_name = "core/taste_dna/password_reset_email.html"
    success_url = reverse_lazy("auth:password_reset_done")
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "registration/password_reset_subject.txt"
    title = _("Password reset")
    token_generator = default_token_generator

    def form_valid(self, form):
        if User.objects.filter(email=form.data.get("email")).exists():
            opts = {
                "use_https": self.request.is_secure(),
                "token_generator": self.token_generator,
                "from_email": self.from_email,
                "email_template_name": self.email_template_name,
                "subject_template_name": self.subject_template_name,
                "request": self.request,
                "html_email_template_name": self.html_email_template_name,
                "extra_email_context": self.extra_email_context,
            }
            form.save(**opts)
            return super().form_valid(form)
        else:
            return render(
                self.request,
                self.template_name,
                context={
                    "error_message": "User does not exit with " "matching email. "
                },
            )


INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"


class UserDeleteView(MyDeleteView):
    """
    View to delete User
    """

    model = User
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_user",)

    def delete(self, request, *args, **kwargs):
        """Override delete method."""
        response = super().delete(request, *args, **kwargs)
        if self.request.is_ajax():
            response_data = {}
            response_data["result"] = True
            response_data["message"] = self.get_success_message()
            return JsonResponse(response_data)
        return response


class UserListAjaxView(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """
    Ajax-Pagination view for OnBoardingQuestion
    """

    model = User
    queryset = model.objects.all().order_by("-id")

    def _get_is_superuser(self, obj):
        """Get boolean column markup."""
        t = get_template("core/partials/list_boolean.html")
        return t.render({"bool_val": obj.is_superuser})

    def is_orderable(self):
        """Check if order is defined in dictionary."""
        return True

    def _get_actions(self, obj):
        """Get actions column markup."""
        t = get_template("core/partials/list_row_actions.html")
        opts = self.model._meta
        return t.render(
            {
                "o": obj,
                "opts": opts,
                "has_change_permission": self.has_change_permission(self.request),
                "has_delete_permission": self.has_delete_permission(self.request),
                "has_view_permission": self.has_view_permission(self.request),
            }
        )

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(email__icontains=self.search) | Q(first_name__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        """Prepare final result data here."""
        # Create row data for data tables
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "email": o.email,
                    "first_name": o.first_name,
                    "username": o.username,
                    "actions": self._get_actions(o),
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        total_filter_data = len(
            self.filter_queryset(self.model.objects.all().order_by("-id"))
        )
        context_data["recordsTotal"] = len(self.model.objects.all().order_by("-id"))
        context_data["recordsFiltered"] = total_filter_data
        return JsonResponse(context_data)
