var Dao = (function($) {
    var Player = {
	add: function(options) {
	    $.ajax({
		url: $SCRIPT_ROOT + '/player',
		type: 'POST',
		dataType: 'json',
		data: { fname: options.fname },
		success: options.success,
		error: options.error
	    });
	},
	remove: function(options) {
	    $.ajax({
		url: $SCRIPT_ROOT + '/player/' + options.player_id,
		type: 'DELETE',
		dataType: 'json',
		success: options.success,
		error: options.error
	    });
	},
	list: function(options) {
	    $.ajax({
		url: $SCRIPT_ROOT + '/player',
		type: 'GET',
		dataType: 'json',
		success: options.success
	    })
	}
    };

    var Tournament = {
	add: function(options) {
	    $.ajax({
		url: $SCRIPT_ROOT + '/tournament',
		type: 'POST',
		dataType: 'json',
		data: { description: options.description },
		success: options.success
	    });
	},
	remove: function(options) {
	    $.ajax({
		url: $SCRIPT_ROOT + '/tournament/' + options.tournament_id,
		type: 'DELETE',
		dataType: 'json',
		success: options.success
	    });
	},
	findByStatus: function(options) {
	    $.ajax({
		url: $SCRIPT_ROOT + '/tournament/status/' + options.status,
		type: 'GET',
		dataType: 'json',
		success: options.success
	    })
	}
    };

    return {
	Player: Player,
	Tournament: Tournament
    }
}(jQuery));
