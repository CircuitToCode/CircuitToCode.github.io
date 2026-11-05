const toggle=document.querySelector(".menu-toggle"),nav=document.querySelector(".nav");
if(toggle&&nav){toggle.addEventListener("click",()=>{const open=nav.classList.toggle("open");toggle.setAttribute("aria-expanded",String(open));});nav.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>{nav.classList.remove("open");toggle.setAttribute("aria-expanded","false");}));}
document.querySelectorAll("#year").forEach(el=>el.textContent=new Date().getFullYear());
const progress=document.getElementById("scrollProgress");
function updateProgress(){if(!progress)return;const max=document.documentElement.scrollHeight-innerHeight;progress.style.width=(max>0?scrollY/max*100:0)+"%";}
addEventListener("scroll",updateProgress,{passive:true});updateProgress();
const revealObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add("visible");revealObserver.unobserve(entry.target);}}),{threshold:.12});
document.querySelectorAll(".reveal").forEach(el=>revealObserver.observe(el));
const filters=document.querySelectorAll(".filter-btn"),cards=document.querySelectorAll(".project-card[data-category]");
filters.forEach(btn=>btn.addEventListener("click",()=>{filters.forEach(x=>x.classList.toggle("active",x===btn));const key=btn.dataset.filter;cards.forEach(card=>card.hidden=key!=="all"&&card.dataset.category!==key);}));
const count=document.getElementById("projectCount");if(count)count.textContent=String(cards.length).padStart(2,"0");
