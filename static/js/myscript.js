const form = document.querySelector('form');
const userTypeSelect = document.querySelector('#user-type');

form.addEventListener('submit', function(event) {
  event.preventDefault(); // prevents form submission so we can handle it with JavaScript

  if (userTypeSelect.value === 'admin') {
    // redirect to admin page
    window.location.href = 'ad_reg.html';
  } else if (userTypeSelect.value === 'agent') {
    // redirect to agent page
    window.location.href = 'ag_reg.html';
  } else {
    // redirect to user page (default)
    window.location.href = 'u_reg.html';
  }
});
