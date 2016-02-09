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

$('#add-player').click(function () {
	$('#init-orderlist').append('<li class="initorder-entry"><span class="init-slot">Player Slot</span> <button type="button" class="close remove pull-right" aria-label="Close"><span aria-hidden="true">&times;</span></button> <span class="pull-right"><span class="eotesymbols">s</span> <input type="number" class="initsuccess-input form-control"><span class="eotesymbols">a</span> <input type="number" class="initadv-input form-control"></span></li>');
})

$('#add-npc').click(function () {
	$('#init-orderlist').append('<li class="initorder-entry"><span class="init-slot">NPC Slot</span> <button type="button" class="close remove pull-right" aria-label="Close"><span aria-hidden="true">&times;</span></button> <span class="pull-right"><span class="eotesymbols">s</span> <input type="number" class="initsuccess-input form-control"><span class="eotesymbols">a</span> <input type="number" class="initadv-input form-control"></span></li>');
})

$(document).on('click', '.remove', function() {
	$(this).parent().remove();
});

var initorder = [];

$('#set-initorder').click(function () {
	initorder = [];
	$( '.initorder-entry').each(function() {
		var initvalue = $(this).find('.initsuccess-input').val() * 100;
		initvalue += $(this).find('.initadv-input').val() * 10;
		if ( $(this).find('.init-slot').text() == 'Player Slot' ) {
			initvalue += 1;
		}
		initorder.push(initvalue);
	});
	initorder.sort().reverse();
	$('.init-entry').remove();
	
	for (i = 0; i < initorder.length; i++) {
		if ( initorder[i] % 2 == 0 ) { // if the value is even, it's a NPC's initiative
			var slottype = 'NPC Slot';
		} else {
			var slottype = 'Player Slot';
		}
		var successes = Math.floor( initorder[i] / 100 );
		var advantages = Math.floor( ( initorder[i] % 100 ) / 10 );
		if ( i == 0 ) {
			var current = "current";
		} else {
			var current = "";
		}
		$('#initiative-list').append('<a class="init-entry ' + current + '" href="#"><li class="initiative-entry"><b>' + slottype + '</b> <span class="pull-right"><span class="eotesymbols">s</span> ' + successes + ' <span class="eotesymbols">a</span> ' + advantages + '</li></a>');
	}
	$('#init-round').html('Round <span id="round-num">1</span>');
	$('#init-setup').modal('hide');
});

$('#init-reset').click(function () {
	$('.init-entry').remove();
	$('#initiative-list').append('<a class="init-entry" href="#"><li class="initiative-entry"><i>Add combatants to start initiative</i></li></a>');
	$('#init-round').html('');
});

$('#init-back').click(function () {
	var current = $('.current');
	if ( $('.current').is(':first-child') ) {
		var round = parseInt( $('#round-num').text() );
		if ( round != 1 ) {
			$('#initiative-list a:last').addClass('current');
			$('#round-num').text( round - 1);
			current.removeClass( 'current' );
		}
	} else {
		$('.current').prev().addClass( 'current' );
		current.removeClass( 'current' );
	}
});

$('#init-next').click(function () {
	var current = $('.current');
	if ( $('.current').is(':last-child') ) {
		$('#initiative-list a:first').addClass('current');
		var round = parseInt( $('#round-num').text() );
		$('#round-num').text( round + 1);
	} else {
		$('.current').next().addClass( 'current' );
	}
	current.removeClass( 'current' );
});
