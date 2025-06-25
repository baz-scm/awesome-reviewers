function setTheme(theme){
  const html=document.documentElement;
  const light=document.querySelector('.toggle-light');
  const dark=document.querySelector('.toggle-dark');
  light.classList.remove('active');
  dark.classList.remove('active');
  if(theme==='light'){
    html.classList.remove('theme-dark');
    html.classList.add('theme-light');
    light.classList.add('active');
  }else{
    html.classList.remove('theme-light');
    html.classList.add('theme-dark');
    dark.classList.add('active');
  }
  localStorage.setItem('theme',theme);
}
document.addEventListener('DOMContentLoaded',()=>{
  const saved=localStorage.getItem('theme')||'dark';
  setTheme(saved);
  document.querySelector('.toggle-light').addEventListener('click',()=>setTheme('light'));
  document.querySelector('.toggle-dark').addEventListener('click',()=>setTheme('dark'));
});
