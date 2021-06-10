function refreshNotifications() {
  $.ajax({
    url: '/beta/notifications',
    method: "GET"
  }).done( function(data) {
    $("#notificationsContainer").html(data);
  });
}

function refreshBoard() {
  $.ajax({
    url: '/beta/top',
    method: "GET"
  }).done( function(data) {
    $('#boardContainer').html(data);
  })
}

function refreshBets() {
  $.ajax({
    url: '/beta/books',
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
  loadTwitch('channel', 'warcraft_with_friends');
  refresh();
  setInterval(refresh(), 10000);
}

function openMenu(name) {
  document.getElementById(name).open();
}

customElements.define('modal-book', class extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
<ion-header>
  <ion-toolbar color="primary">
    <ion-title>开盘</ion-title>
    <ion-buttons slot="primary">
      <ion-button onClick="dismissModal()">
        <ion-icon slot="icon-only" name="close"></ion-icon>
      </ion-button>
    </ion-buttons>
  </ion-toolbar>
</ion-header>
<ion-content>
<form action="/book" method="post">
  <ion-grid>
    <ion-row>
      <ion-col size="6">
        <ion-item lines="full">
          <ion-label position="stacked">队伍1</ion-label>
          <ion-input required type="text" placeholder="team1" name="player1" id="player1" form="bookForm"></ion-input>
        </ion-item>
      </ion-col>
      <ion-col size="6">
        <ion-item lines="full">
          <ion-label position="stacked">队伍2</ion-label>
          <ion-input required type="text" placeholder="team2" name="player1" id="player2" form="bookForm"></ion-input>
        </ion-item>
      </ion-col>
    </ion-row>
    <ion-row>
      <ion-col size="6">
        <ion-item lines="full">
          <ion-label position="stacked">赔率1</ion-label>
          <ion-input required type="number" min="0.01" max="9.99" step="0.01" placeholder="0.1" name="odd1" id="odd1" form="bookForm"></ion-input>
        </ion-item>
      </ion-col>
      <ion-col size="6">
        <ion-item lines="full">
          <ion-label position="stacked">赔率2</ion-label>
          <ion-input required type="number" min="0.01" max="9.99" step="0.01" placeholder="0.1" name="odd2" id="odd2" form="bookForm"></ion-input>
        </ion-item>
      </ion-col>
      <ion-col size="6">
        <ion-item lines="full">
          <ion-label position="stacked">金额</ion-label>
          <ion-input required type="number" min="300" step ="50" placeholder="300" name="gae" id="gae" form="bookForm"></ion-input>
        </ion-item>
      </ion-col>
    </ion-row>
  </ion-grid>
  <ion-button size="large" style="position: fixed; bottom: 10; left: 10; right: 10" color="tertiary" type="submit" form="bookForm">
    <ion-label class="ion-text-center">开盘</ion-label>
  </ion-button>
  </form>
</ion-content>
`;
  }
});

function dismissModal() {
  document.getElementsByTagName('ion-modal').item(0).dismiss();
}

function presentBook() {
  // create the modal with the `modal-page` component
  const modalElement = document.createElement('ion-modal');
  modalElement.component = 'modal-book';
  modalElement.cssClass = 'my-custom-class';

  // present the modal
  document.body.appendChild(modalElement);
  return modalElement.present();
}

function loadTwitch(type, id) {
  $.ajax({
    url: '/beta/twitch',
    method: "GET",
    data: {
        type: type,
        tid: id
    }
  }).done( function(data) {
    console.log("Loaded twitch", data);
    $('#videoContainer').html(data);
  })
}

function loadBet(bid) {
  $.ajax({
    url: '/beta/bet',
    method: "GET",
    data: {
      bid: bid
    }
  }).done( function(data) {
    $('#betContainer').html(data[0]);
    if (data.length > 1) {
      $('#videoContainer').html(data[1]);
    }
  })
}