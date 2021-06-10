function refreshNotifications() {
  $.ajax({
    url: '/notifications',
    method: "GET"
  }).done( function(data) {
    $("#notificationsContainer").html(data);
  });
}

function refreshBoard() {
  $.ajax({
    url: '/top',
    method: "GET"
  }).done( function(data) {
    $('#boardContainer').html(data);
  })
}

function refreshBets() {
  $.ajax({
    url: '/books',
    method: "GET"
  }).done( function(data) {
    console.log(data);
    $('#betsContainer').html(data);
  })
}

function refresh() {
  console.log("Refreshed data");
  refreshNotifications();
  refreshBoard();
  refreshBets();
}

function initialize() {
  refresh();
  setInterval(refresh(), 10000);
}