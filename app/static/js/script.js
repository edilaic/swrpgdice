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
				var date = new Date()
				var roll = "<div class='roll-entry'><table class='table roll-table'><tr><td class='player'><span class='name'>" + data["player"] + "</span> rolled: </td>";
				var totalstring = data["total"];
				roll += "<td class='roll-results'>" + totalstring + "</td>";
				roll += "<td class='dice-rolls'>"
				$(dice).each(function (i) {
						roll += "<img src='/static/swdice/" + dice[i] + ".png' /> ";
				})
				roll += "</td></table></div>";
				$('#placeholder').prepend(roll);
		});
		// event handler for new connections
		socket.on('connect', function() {
				return false;
		});
});

$('#reset-dice').click(function (e) {
	e.preventDefault()
	$('.dice-input').val('');
})
