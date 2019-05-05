$(function () {
    // Setup CSRF token in ajax
    // $.ajaxSetup({
    //     beforeSend: function(xhr, settings) {
    //         if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
    //             xhr.setRequestHeader("X-CSRFToken", csrfToken);
    //         }
    //     }
    // });
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
    
    // Install date picker for the target date
    $('#datepick').datetimepicker({
        format: 'L',
	minDate: moment(),
	useCurrent: false,
        inline: true,
        sideBySide: true,
	icons: {
	    time: 'far fa-clock',
	    date: 'far fa-calendar-alt',
	    up: 'fas fa-arrow-up',
	    down: 'fas fa-arrow-down',
	    previous: 'fas fa-chevron-left',
	    next: 'fas fa-chevron-right',
	    today: 'far fa-calendar-check',
	    clear: 'far fa-trash-alt',
	    close: 'fas fa-times'
	}
    });

    $(document).ready(function() {
	$('.nav-trigger').click(function() {
	    $('.side-nav').toggleClass('visible');
	});
    });

    // App logic
    var grid, dialog;

    // Form cleanup
    function clearForm(form) {
	$(form).find("input[type=text], textarea").val('');
    }

    // Reset form title and button back to the orignal
    $('#feature-modal-form').on('hide.bs.modal', function(e) {
	$("#new-feature-request-title").show();
	$("#edit-feature-request-title").hide();
	clearForm('#feature-modal-form');
    });
    
    // Edit Feature Request
    function Edit(e) {
	// Reuse the create form
	$("#new-feature-request-title").hide();
	$("#edit-feature-request-title").show();
	
	$("#feature-request-id").val(e.data.record.id);
	$('#title').val(e.data.record.title);
	$('#description').val(e.data.record.description);
	$('input[name=target_date').val(e.data.record.target_date);
	$('#client').val(e.data.record.client_id);
	$('#client_priority').val(e.data.record.client_priority);
        $('#product_area_id').val(e.data.record.product_area_id);
	saveURL = editURL; // Tell the form to submit it to the edit endpoint URL.
	$('#feature-modal-form').modal('show');
    }

    // Save works for both Create and Edit form
    function Save(e) {
	// saveURL is a switch used to check whether this is a new feature request or an edit.
	if (saveURL === undefined) {
	    saveURL = newURL;
	}
	
	$.ajax({
            type: "POST",
            url: saveURL,
            data: $('#feature-request-form').serialize(),
            success: function (data) {
                grid.reload();
		$('#feature-modal-form').modal('hide');
		clearForm('#feature-modal-form');
            },
	    failure: function () {
                alert('Failed to save.');
		$('#feature-modal-form').modal('hide');
	    }
        });
	saveURL = newURL;
        e.preventDefault();
    }

    // Delete will delete a feature request and reload the grid
    function Delete(e) {
        if (confirm('Are you sure?')) {
	    console.log(e.data.id);
            $.ajax({ url: '/delete', data: { id: e.data.id }, method: 'POST' })
                .done(function () {
                    grid.reload();
                })
                .fail(function () {
                    alert('Failed to delete.');
                });
        }
    }

    // getDetails is triggered whenever a grid rown is clicked.
    // It takes the values of the record and display in the description panel
    function getDetails(e, $row, id, record) {
        $('#feature-title').text(record.title);
        $('#feature-priority').text(record.client_priority);
        $('#feature-target-date').text(record.target_date);
        $('#feature-client').text(record.client);
        $('#feature-product-area').text(record.product_area_name);
	$('#feature-description').text(record.description);
    }

    // Grid setup.
    grid = $('#grid').grid({
        primaryKey: 'id',
        dataSource: '/list',
        uiLibrary: 'bootstrap4',
        columns: [
            { field: 'id', width: 48 },
            { field: 'title', title: 'Title', width: 350, sortable: true },
            { field: 'description', hidden: true },
            { field: 'target_date', hidden: true },
            { field: 'client', title: 'Client', sortable: true },
	    { field: 'client_priority', title: 'Priority', sortable: true },
	    { field: 'product_area_id', hidden: true },
	    { field: 'product_area_name', hidden: true },
            { title: '', field: 'Edit', width: 42, type: 'icon', icon: 'fa fa-pen-square', tooltip: 'Edit', events: { 'click': Edit } },
            { title: '', field: 'Delete', width: 42, type: 'icon', icon: 'fa fa-minus-square', tooltip: 'Delete', events: { 'click': Delete } }
        ],
        pager: { limit: 5, sizes: [2, 5, 10, 20] }
    });

    // Display details of the selected feature request.
    grid.on('rowSelect', getDetails);

    // Handle feature request detail upon load
    grid.on('dataBound', function(e, records, totalRecords) {
	if (totalRecords > 0) {
	    // get the details of the first record and render its details
	    var record = records[0];
            $('#feature-title').text(record.title);
            $('#feature-priority').text(record.client_priority);
            $('#feature-target-date').text(record.target_date);
            $('#feature-client').text(record.client);
            $('#feature-product-area').text(record.product_area_name);
	    $('#feature-description').text(record.description);
	    $('.feature-request-details').show();
	} else {
	    $('.feature-request-details').hide();
	}
    });

    // Persist data.
    $('#feature-request-form').submit(Save);

    // Simple search.
    $('#search-feature').on('click', function () {
        grid.reload({ title: $('#feature-request-title').val() });
    });

    // Clear search.
    $('#clear-search').on('click', function () {
        $('#feature-request-title').val('');
        grid.reload({ title: ''});
    });

    // Sidenav filters
    $('.feature-nav-by-client a').on('click', function (e) {
	var client_id = $(this).attr('data-query-client');
	// FIXME: Can't find a way to clear the ajax params. Doing it by hand here.
	delete grid.data().params['client_priority']
        grid.reload({ client_id: client_id});
	e.preventDefault();
    });    

    $('.feature-nav-by-priority a').on('click', function (e) {
	var client_priority = $(this).attr('data-query-priority');
	// FIXME: Can't find a way to clear the ajax params. Doing it by hand here.
	delete grid.data().params['client_id']
        grid.reload({client_priority: client_priority});
	e.preventDefault();
    });
    
});
