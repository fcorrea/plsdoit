$(function () {
    $('#datepick').datetimepicker({
        format: 'L',
	minDate: moment(),
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
});
