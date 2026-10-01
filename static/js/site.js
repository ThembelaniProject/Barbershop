function toggleMenu(){
  const nav=document.getElementById("nav");
  const button=document.querySelector(".menu");
  if(!nav||!button)return;
  const open=nav.classList.toggle("open");
  button.setAttribute("aria-expanded",String(open));
  button.setAttribute("aria-label",open?"Close navigation":"Open navigation");
}
function closeOffer(){
  const offer=document.getElementById("offer");
  if(offer)offer.remove();
}
setTimeout(()=>{
  const offer=document.getElementById("offer");
  if(offer)offer.classList.add("show");
},600);
document.addEventListener("keydown",(event)=>{
  if(event.key==="Escape"){
    const nav=document.getElementById("nav");
    const button=document.querySelector(".menu");
    if(nav&&nav.classList.contains("open")){
      nav.classList.remove("open");
      if(button){button.setAttribute("aria-expanded","false");button.setAttribute("aria-label","Open navigation");}
    }
  }
});
document.addEventListener("click",(event)=>{
  const nav=document.getElementById("nav");
  const button=document.querySelector(".menu");
  if(!nav||!button||!nav.classList.contains("open"))return;
  if(!nav.contains(event.target)&&!button.contains(event.target)){
    nav.classList.remove("open");
    button.setAttribute("aria-expanded","false");
    button.setAttribute("aria-label","Open navigation");
  }
});
