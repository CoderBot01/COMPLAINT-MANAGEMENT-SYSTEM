// Get references to the navbar buttons and content sections
const welcomeBtn = document.querySelector('#welcome-btn');
const checkComplainBtn = document.querySelector('#check-complain-btn');
const addUserBtn = document.querySelector('#add-user-btn');
const checkUserStatusBtn = document.querySelector('#check-user-status-btn');
const welcomeSection = document.querySelector('#welcome-section');
const checkComplainSection = document.querySelector('#check-complain-section');
const addUserSection = document.querySelector('#add-user-section');
const checkUserStatusSection = document.querySelector('#check-user-status-section');

// Add click event listeners to the navbar buttons
welcomeBtn.addEventListener('click', () => {
  welcomeSection.style.display = 'block';
  checkComplainSection.style.display = 'none';
  addUserSection.style.display = 'none';
  checkUserStatusSection.style.display = 'none';
});

checkComplainBtn.addEventListener('click', () => {
  welcomeSection.style.display = 'none';
  checkComplainSection.style.display = 'block';
  addUserSection.style.display = 'none';
  checkUserStatusSection.style.display = 'none';
});

addUserBtn.addEventListener('click', () => {
  welcomeSection.style.display = 'none';
  checkComplainSection.style.display = 'none';
  addUserSection.style.display = 'block';
  checkUserStatusSection.style.display = 'none';
});

checkUserStatusBtn.addEventListener('click', () => {
  welcomeSection.style.display = 'none';
  checkComplainSection.style.display = 'none';
  addUserSection.style.display = 'none';
  checkUserStatusSection.style.display = 'block';
});