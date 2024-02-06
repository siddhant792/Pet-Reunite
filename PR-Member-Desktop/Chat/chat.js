import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js'
import { getFirestore, setDoc, where, doc, collection, addDoc, onSnapshot, query, or, orderBy } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js'

const user = JSON.parse(localStorage.getItem("user"));
const firebaseConfig = {
  apiKey: "AIzaSyCaUhqgDgMCWlzIgbsUCReo2efQQzIBDM8",
  authDomain: "pet-reunite-410804.firebaseapp.com",
  projectId: "pet-reunite-410804",
  storageBucket: "pet-reunite-410804.appspot.com",
  messagingSenderId: "814398700325",
  appId: "1:814398700325:web:90841c736068f98ac9f8cc"
};
initializeApp(firebaseConfig);

const userId = user._id;
const firestore = getFirestore();

const collectionRef = collection(firestore, `users/${userId}/activeChats`);
const userListQuery = query(collectionRef, orderBy("lastInteraction", "desc"));
const chatCont = document.getElementById("messages");
const userList = document.getElementById("user-list");

const chatSection = document.getElementById("chat-section")
const chatPlaceholder = document.getElementById("chat-placeholder")
chatSection.style.display = "none";

var activeChatUserId = getQueryParam('user_id') || "";
var activeChatUserName = getQueryParam('user_name');

if (activeChatUserId != "") {
  chatSection.style.display = "block";
  chatPlaceholder.style.display = "none";
  handleItemClick(activeChatUserName, activeChatUserId);
}

function handleItemClick(name, id) {
  activeChatUserId = id;
  activeChatUserName = name;
  chatCont.innerHTML = '';
  document.getElementById("active-chat-user-name").innerHTML = name;
  const ref = collection(firestore, `chats`);
  const messageQuery = query(ref, or(where("identifier", "==", userId + id), where("identifier", "==", id + userId)), orderBy("timestamp"));
  onSnapshot(messageQuery, (querySnapshot) => {
    chatCont.innerHTML = '';
    querySnapshot.forEach((doc) => {
      const msg = doc.data()
      const chatMsg = document.createElement("div");
      const dir = msg.sender == userId ? 'sent' : 'received';
      chatMsg.innerHTML = `
        <div class="message ${dir}">
          <span class="bubble">${msg.message}</span>
        </div>
      `;

      chatCont.appendChild(chatMsg);
    });
  });
}

// populating the chat list
onSnapshot(userListQuery, (querySnapshot) => {
  userList.innerHTML = "";
  querySnapshot.forEach((doc) => {
    const userData = doc.data()
    const userListItem = document.createElement("div");
    userListItem.classList.add("user-list-item");

    userListItem.innerHTML = `
      <img src="https://cdn-icons-png.flaticon.com/512/219/219988.png" alt="Profile" class="profile-picture" />
      <div class="user-info">
        <h3>${userData.name}</h3>
      </div>
    `;

    userListItem.onclick = () => {
      chatSection.style.display = "block";
      chatPlaceholder.style.display = "none";
      handleItemClick(userData.name, userData.user_id);
    }

    userList.appendChild(userListItem);
  });
});


document.getElementById("send-message").onclick = (event) => {
  const draft = document.getElementById("message-draft");
  if(draft.value !== "") {
    addDoc(collection(firestore, `chats`), {
      "message": draft.value,
      "sender": userId,
      "receiver": activeChatUserId,
      "timestamp": new Date().toISOString(),
      "identifier": userId + activeChatUserId
    });

    setDoc(doc(firestore, `users/${userId}/activeChats`, activeChatUserId), {
      'lastInteraction': new Date().toISOString(),
      'name': activeChatUserName,
      'user_id': activeChatUserId
    });

    setDoc(doc(firestore, `users/${activeChatUserId}/activeChats`, userId), {
      'lastInteraction': new Date().toISOString(),
      'name': user.first_name + " " + user.last_name,
      'user_id': userId
    });
  
    draft.value = "";
  }
};

function getQueryParam(name) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(name);
}

