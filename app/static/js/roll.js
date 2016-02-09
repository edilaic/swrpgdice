$('#reset-dice').click(function (e) {
	e.preventDefault();
	$('.dice-input').val('');
});

$('#destiny-point').click(function (e) {
    e.preventDefault();
    $.get( "/destiny", {
        player: $('#player').val(),
        side: "light"
    });
});

$('#destiny-point-dark').click(function (e) {
    e.preventDefault();
    $.get( "/destiny", {
        player: $('#player').val(),
        side: "dark"
    });
});

$('#set-destiny-dice').click(function (e) {
    e.preventDefault();
    $.get( "/setdestiny", {
        dark: $('#dark').val(),
        light: $('#light').val()
    });
});
