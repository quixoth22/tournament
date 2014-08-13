App = Ember.Application.create();

App.Router.map(function() {
    this.route("tournaments");
    this.route("tournaments", {path: "/"});
    this.route("players", { path: "/players" });
});

App.IndexRoute = Ember.Route.extend({
  model: function() {
      return this.store.find('tournament');
  }
});

App.TournamentsRoute = Ember.Route.extend({
    model: function() {
        return this.store.find('tournament');
    }
});

App.PlayersRoute = Ember.Route.extend({
    model: function() {
        return this.store.find('player');
    }
});
