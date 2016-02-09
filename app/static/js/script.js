$(document).ready(function(){
	// change to an empty string to use the global namespace
	// the socket.io documentation recommends sending an 
	// explicit package upon connection
	// this is specially important when using the global namespace
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/swdice');

	// event handler for server sent data
	// the data is displayed in the "Received" section of the page
	socket.on('edroll', function(msg) {
		var data = $.parseJSON(msg.data);
		var dice = data["dice"];
		var roll = "<div class='roll-entry'><table class='table roll-table'><tr><td class='player'><span class='name'>" + data["player"] + "</span> rolled: </td>";
		var totalstring = data["total"];
		roll += "<td class='roll-results'>" + totalstring + "</td>";
		roll += "<td class='dice-rolls'>"
		$(dice).each(function (i) {
			roll += "<img src='/static/swdice/" + dice[i] + ".png' /> ";
		});
		roll += "</td></table></div>";
		$('#placeholder').prepend(roll);
	});

	socket.on('destiny', function(msg) {
		var data = $.parseJSON(msg.data);
		var light = data["light"];
		var dark = data["dark"];
		var change = data["change"];
		var roll = "<div class='roll-entry'><table class='table roll-table'><tr><td class='player'><span class='name'>" + data["player"] + "</span></td>";
		roll += "<td class='roll-results'>" + change + "</td>";
		roll += "</table></div>";
		$('#placeholder').prepend(roll);
        $('#destiny-dark p').html("");
        for (i = 0; i < data["dark"]; i++) {
            $('#destiny-dark p').prepend('<span class="eotesymbols die-setback">z</span>');
        }
        $('#destiny-light p').html("");
        for (i = 0; i < data["light"]; i++) {
            $('#destiny-light p').prepend('<span class="eotesymbols die-force">z</span>');
        }
	});

	socket.on('setdestiny', function(msg) {
		var data = $.parseJSON(msg.data);
		var light = data["light"];
		var dark = data["dark"];
		var change = data["change"];
		var roll = "<div class='roll-entry'><table class='table roll-table'>";
		roll += "<td class='roll-results'>" + change + "</td>";
		roll += "</table></div>";
		$('#placeholder').prepend(roll);
        $('#destiny-dark p').html("");
        for (i = 0; i < data["dark"]; i++) {
            $('#destiny-dark p').prepend('<span class="eotesymbols die-setback">z</span>');
        }
        $('#destiny-light p').html("");
        for (i = 0; i < data["light"]; i++) {
            $('#destiny-light p').prepend('<span class="eotesymbols die-force">z</span>');
        }
	});

	// event handler for new connections
	socket.on('connect', function() {
		return false;
	});
});
