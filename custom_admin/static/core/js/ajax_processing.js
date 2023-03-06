/*global $ */
'use strict';

$(document).ready(function () {



    $('#employee-table').DataTable({
        pageLength: 10,
        responsive: true,
        order: [[0, "desc"]],
        columnDefs: [{
            orderable: false,
            targets: -1
        },],
        "language":
        {
            "processing": "<b><i class='fa fa-refresh fa-spin'></i>&nbsp;Loading....</b>",
        },
        // Ajax for pagination
        processing: true,
        serverSide: true,
        ajax: {
            url: window.pagination_url,
            type: 'get',
        },
        columns: [
            { data: 'id', name: 'id' },
            { data: 'name', name: 'name' },
            { data: 'employee_id', name: 'employee_id' },
            { data: 'phone_number', name: 'phone_number' },
            { data: 'address', name: 'address' },
            { data: 'actions', name: 'actions' },
        ],
    });


    $('#user-table').DataTable({
        pageLength: 10,
        responsive: true,
        order: [[0, "desc"]],
        columnDefs: [{
            orderable: false,
            targets: -1
        },],
        "language":
        {
            "processing": "<b><i class='fa fa-refresh fa-spin'></i>&nbsp;Loading....</b>",
        },
        // Ajax for pagination
        processing: true,
        serverSide: true,
        ajax: {
            url: window.pagination_url,
            type: 'get',
        },
        columns: [
            { data: 'id', name: 'id' },
            { data: 'email', name: 'email' },
            { data: 'first_name', name: 'first_name' },
            { data: 'username', name: 'username' },
            { data: 'actions', name: 'actions' }
        ],
    });
});