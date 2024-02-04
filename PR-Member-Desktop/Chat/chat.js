import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js'
import { getFirestore, doc, where, collection, addDoc, onSnapshot, query, or, orderBy } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js'

const firebaseConfig = {
  apiKey: "AIzaSyCaUhqgDgMCWlzIgbsUCReo2efQQzIBDM8",
  authDomain: "pet-reunite-410804.firebaseapp.com",
  projectId: "pet-reunite-410804",
  storageBucket: "pet-reunite-410804.appspot.com",
  messagingSenderId: "814398700325",
  appId: "1:814398700325:web:90841c736068f98ac9f8cc"
};

initializeApp(firebaseConfig);

const userId = "Jsdp3xfxfBl0EFVDSU54";
const firestore = getFirestore();

const chatSection = document.getElementById("chat-section")
const chatPlaceholder = document.getElementById("chat-placeholder")
chatSection.style.display = "none";

var activeChatUserId = "";

function handleItemClick(name, id) {
  activeChatUserId = id;
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

const collectionRef = collection(firestore, `users/${userId}/activeChats`);
const userListQuery = query(collectionRef, orderBy("lastInteraction", "desc"));
const chatCont = document.getElementById("messages");
const userList = document.getElementById("user-list");
// populating the chat list
onSnapshot(userListQuery, (querySnapshot) => {
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
  
    draft.value = "";
  }
};
