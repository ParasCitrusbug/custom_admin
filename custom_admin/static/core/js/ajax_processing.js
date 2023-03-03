/*global $ */
'use strict';

$(document).ready(function () {

    $('#onboardingquestion-table').DataTable({
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
            { data: 'statement', name: 'statement', id: "draggable" },
            { data: 'order', name: 'order' },
            { data: 'question_type', name: 'question_type' },
            { data: 'question_category', name: 'question_category' },
            { data: 'option', name: 'option' },
            { data: 'is_active', name: 'is_active' },
            { data: 'actions', name: 'actions' },
        ],
    });

    $('#foodorigin-table').DataTable({
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
            { data: 'name', name: 'name' },
            { data: 'is_active', name: 'is_active' },
            { data: 'actions', name: 'actions' },
        ],
    });

    $('#foodingredient-table').DataTable({
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
            { data: 'name', name: 'name' },
            { data: 'is_active', name: 'is_active' },
            { data: 'actions', name: 'actions' },
        ],
    });

    $('#foodcuisine-table').DataTable({
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
            { data: 'name', name: 'name' },
            { data: 'is_active', name: 'is_active' },
            { data: 'actions', name: 'actions' },
        ],
    });

    $('#article-table').DataTable({
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
            { data: 'title', name: 'title' },
            { data: 'description', name: 'description' },
            { data: 'is_active', name: 'is_active' },
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