"""
This is a view module to define list, create, update, delete views.
You can define different view properties here.
"""
from django.db.models import Q
from django_datatables_too.mixins import DataTableMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import get_template

from custom_admin.mixins import HasPermissionsMixin
from custom_admin.forms.employees import MyEmployeeCreationForm, EmployeeChangeForm
from custom_admin.views.generic import (
    MyLoginRequiredView,
    MyUpdateView,
    MyListView,
    MyDetailView,
    MyDeleteView,
    MyCreateView,
)
from employee.models import Employee


class EmployeeDetailView(MyDetailView):
    """
    View for employee details
    """

    model = Employee
    template_name = "core/adminemployee/employee_details.html"
    permission_required = ("core.view_user",)

    def get(self, request, pk):
        """Get Employee data"""
        context = {}
        employee_data = Employee.objects.get(pk=pk)
        context["employee_data"] = employee_data

        return render(request, self.template_name, context)


class EmployeeListView(MyListView):
    """
    View for employee listing
    """

    ordering = ["id"]
    model = Employee
    template_name = "core/adminemployee/employee_list.html"
    permission_required = ("core.view_user",)


class EmployeeCreateView(MyCreateView):
    """
    View to create Employee
    """

    model = Employee
    form_class = MyEmployeeCreationForm
    template_name = "core/adminemployee/employee_forms.html"
    permission_required = ("core.add_user",)

    def get_context_data(self, **kwargs):
        """Get context data"""

        context = super(EmployeeCreateView, self).get_context_data()
        return context


class EmployeeUpdateView(MyUpdateView):
    """
    View to update Employee
    """

    model = Employee
    form_class = EmployeeChangeForm
    template_name = "core/adminemployee/employee_forms.html"
    permission_required = ("core.change_user",)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class EmployeeDeleteView(MyDeleteView):
    """
    View to delete Employee
    """

    model = Employee
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


class EmployeeListAjaxView(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """
    Ajax-Pagination view for Employee
    """

    model = Employee
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
                Q(name__icontains=self.search) | Q(address__icontains=self.search)
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
                    "name": o.name,
                    "employee_id": o.employee_id,
                    "phone_number": o.phone_number,
                    "address": o.address,
                    "working": o.working,
                    "department": o.department,
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
