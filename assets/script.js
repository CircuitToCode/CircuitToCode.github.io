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


/* Live public GitHub activity — no token is exposed in the browser. */
(async function loadGitHubActivity(){
  const target=document.getElementById("githubActivity");
  const updated=document.getElementById("githubUpdated");
  if(!target)return;
  const username="CircuitToCode";
  const cacheKey="ctc-github-events-v1";
  const labels={PushEvent:["↥","Pushed commits"],PullRequestEvent:["⑂","Pull request"],IssuesEvent:["◎","Issue activity"],IssueCommentEvent:["✎","Commented"],CreateEvent:["＋","Created"],WatchEvent:["★","Starred"],ForkEvent:["⑃","Forked"],ReleaseEvent:["◈","Released"],PublicEvent:["◉","Made public"]};
  const ago=value=>{const sec=Math.max(0,Math.floor((Date.now()-new Date(value).getTime())/1000));if(sec<60)return "just now";if(sec<3600)return Math.floor(sec/60)+"m ago";if(sec<86400)return Math.floor(sec/3600)+"h ago";if(sec<604800)return Math.floor(sec/86400)+"d ago";return Math.floor(sec/604800)+"w ago";};
  const render=events=>{
    const rows=events.filter(e=>labels[e.type]).slice(0,8);
    if(!rows.length){target.innerHTML='<div class="github-empty">No recent public activity to display yet.</div>';return;}
    target.innerHTML=rows.map(e=>{const [symbol,label]=labels[e.type];const repo=e.repo?.name||username;const url="https://github.com/"+repo;let detail=label;if(e.type==="PushEvent")detail=(e.payload?.commits?.length||1)+" commit(s)";if(e.type==="PullRequestEvent")detail=(e.payload?.action||"updated")+" pull request";if(e.type==="IssuesEvent")detail=(e.payload?.action||"updated")+" issue";return '<article class="github-event"><span class="github-event-icon">'+symbol+'</span><div class="github-event-copy"><strong>'+detail+'</strong><small><a href="'+url+'" target="_blank" rel="noopener">'+repo+'</a></small></div><time datetime="'+e.created_at+'">'+ago(e.created_at)+'</time></article>';}).join("");
    if(updated)updated.textContent="Last refreshed "+new Date().toLocaleTimeString()+" · Source: GitHub public events";
  };
  try{
    const cached=sessionStorage.getItem(cacheKey);
    if(cached)render(JSON.parse(cached));
    const response=await fetch("https://api.github.com/users/"+username+"/events/public?per_page=30",{headers:{Accept:"application/vnd.github+json"}});
    if(!response.ok)throw new Error("GitHub API returned "+response.status);
    const events=await response.json();
    sessionStorage.setItem(cacheKey,JSON.stringify(events));
    render(events);
  }catch(error){
    if(!target.querySelector(".github-event"))target.innerHTML='<div class="github-empty github-error">Live activity is temporarily unavailable. <a href="https://github.com/'+username+'" target="_blank" rel="noopener">View GitHub profile ↗</a></div>';
    if(updated)updated.textContent="Live feed requires a connection to GitHub; profile link remains available.";
  }
})();


/* Rotating professional identity */
(function(){const el=document.getElementById("roleRotator");if(!el)return;const roles=["Embedded Engineer","Industrialization Engineer","Electronics Developer","Automation Enthusiast"];let i=0;setInterval(()=>{el.classList.add("role-out");setTimeout(()=>{i=(i+1)%roles.length;el.textContent=roles[i];el.classList.remove("role-out");},220);},2600);})();
