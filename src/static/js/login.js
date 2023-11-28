const signUpBtn = document.getElementById('signUp'),
  signInBtn = document.getElementById('signIn'),
  container = document.getElementById('container');

signUpBtn.addEventListener('click', () => {
  container.classList.add('right-panel-active');
});
signInBtn.addEventListener('click', () => {
  container.classList.remove('right-panel-active');
});