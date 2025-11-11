// Simple local storage helpers
const getData = (key, fallback) => JSON.parse(localStorage.getItem(key)) || fallback;
const setData = (key, value) => localStorage.setItem(key, JSON.stringify(value));

// -------------------- LIKE BUTTON --------------------
const likeButton = document.getElementById("like-button");
const likeCount = document.getElementById("like-count");

let likes = getData("likes", 0);
likeCount.textContent = likes;

likeButton.addEventListener("click", () => {
  likes++;
  likeCount.textContent = likes;
  setData("likes", likes);
});

// -------------------- COMMENTS --------------------
const commentList = document.getElementById("comment-list");
const newComment = document.getElementById("new-comment");
const addCommentBtn = document.getElementById("add-comment");

let comments = getData("comments", []);

function renderComments() {
  if (comments.length === 0) {
    commentList.innerHTML = "<p>No comments yet. Be the first to share your thoughts!</p>";
  } else {
    commentList.innerHTML = comments
      .map(comment => `<p>💬 ${comment}</p>`)
      .join("");
  }
}
renderComments();

addCommentBtn.addEventListener("click", () => {
  const text = newComment.value.trim();
  if (text !== "") {
    comments.push(text);
    setData("comments", comments);
    newComment.value = "";
    renderComments();
  }
});

// -------------------- SEARCH --------------------
const searchInput = document.getElementById("search-input");
const searchButton = document.getElementById("search-button");
const searchResults = document.getElementById("search-results");

// Example verse history (will later pull from data/verses.json)
const verseHistory = [
  { reference: "Psalm 23:1", text: "The Lord is my shepherd; I have what I need." },
  { reference: "John 3:16", text: "For God so loved the world..." },
  { reference: "Isaiah 40:31", text: "Those who trust in the Lord will renew their strength." },
];

searchButton.addEventListener("click", () => {
  const query = searchInput.value.trim().toLowerCase();
  if (query === "") {
    searchResults.innerHTML = "<p>Please enter a verse or keyword to search.</p>";
    return;
  }

  const results = verseHistory.filter(v =>
    v.reference.toLowerCase().includes(query) ||
    v.text.toLowerCase().includes(query)
  );

  if (results.length > 0) {
    searchResults.innerHTML = results
      .map(r => `<p><strong>${r.reference}</strong>: ${r.text}</p>`)
      .join("");
  } else {
    searchResults.innerHTML = "<p>No matching verses found.</p>";
  }
});

// -------------------- REQUEST SECTION --------------------
const requestInput = document.getElementById("request-input");
const sendRequest = document.getElementById("send-request");
const requestConfirmation = document.getElementById("request-confirmation");

sendRequest.addEventListener("click", () => {
  const requestText = requestInput.value.trim();
  if (requestText !== "") {
    const requests = getData("requests", []);
    requests.push({ text: requestText, date: new Date().toISOString() });
    setData("requests", requests);
    requestInput.value = "";
    requestConfirmation.classList.remove("hidden");
    requestConfirmation.textContent = "Request sent! 💌";
    setTimeout(() => requestConfirmation.classList.add("hidden"), 3000);
  }
});

