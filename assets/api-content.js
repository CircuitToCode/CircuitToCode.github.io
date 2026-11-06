(function(){
  const base=(window.PORTFOLIO_API_BASE_URL||"").trim().replace(/\/$/,"");
  if(!base)return;
  const endpoint=base+"/api/v1/projects";
  const esc=value=>String(value??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const categoryOf=value=>{
    const v=String(value||"").toLowerCase();
    if(/embed|firmware|electronics|microcontroller/.test(v))return "embedded";
    if(/software|app|web|data|python|automation tool/.test(v))return "software";
    return "engineering";
  };
  const projectHref=p=>{
    const slug=String(p.slug||"").trim();
    return slug ? "projects/"+encodeURIComponent(slug)+".html" : "projects.html#project-library";
  };
  const artClass=p=>{
    const c=categoryOf(p.category);
    return c==="embedded"?"project-embedded":c==="software"?"project-data":"project-process";
  };
  const imageMarkup=p=>p.image_url
    ? '<div class="project-art api-project-art"><img loading="lazy" src="'+esc(/^https?:\/\//i.test(p.image_url)?p.image_url:base+p.image_url)+'" alt=""></div>'
    : '<div class="project-art api-project-art"><div class="art-code">{ }</div><b>'+esc(String(p.category||"ENGINEERING").toUpperCase())+'</b></div>';
  function homepage(projects){
    const grid=document.querySelector(".cinema-project-grid");
    if(!grid)return;
    const items=projects.filter(p=>p.featured).slice(0,6);
    if(!items.length)return;
    grid.innerHTML=items.map((p,i)=>'<a class="cinema-project '+artClass(p)+' reveal" href="'+esc(projectHref(p))+'"><span>'+String(i+1).padStart(2,"0")+' / '+esc(String(p.category||"PROJECT").toUpperCase())+'</span>'+imageMarkup(p)+'<h3>'+esc(p.title)+'</h3><p>'+esc(p.description)+'</p><i class="project-open">VIEW PROJECT ↗</i></a>').join("");
    grid.querySelectorAll(".reveal").forEach(el=>el.classList.add("visible"));
  }
  function library(projects){
    const grid=document.querySelector(".projects-grid");
    if(!grid)return;
    if(!projects.length)return;
    grid.innerHTML=projects.map((p,i)=>'<a class="project-card" data-category="'+categoryOf(p.category)+'" href="'+esc(projectHref(p))+'"><div class="project-visual '+(categoryOf(p.category)==="embedded"?"visual-ev":categoryOf(p.category)==="software"?"visual-software":"visual-process")+'">'+(p.image_url?'<img loading="lazy" src="'+esc(/^https?:\/\//i.test(p.image_url)?p.image_url:base+p.image_url)+'" alt="">':"")+'<span>'+String(i+1).padStart(2,"0")+' / '+esc(String(p.category||"PROJECT").toUpperCase())+'</span><b>'+esc(p.title)+'</b></div><div class="project-info"><h3>'+esc(p.title)+'</h3><p>'+esc(p.description)+'</p><span class="card-arrow">OPEN PROJECT ↗</span></div></a>').join("");
    const count=document.getElementById("projectCount");if(count)count.textContent=String(projects.length).padStart(2,"0");
    grid.querySelectorAll(".project-card").forEach(card=>{});
  }
  fetch(endpoint,{headers:{Accept:"application/json"}})
    .then(r=>{if(!r.ok)throw new Error("Projects API returned "+r.status);return r.json();})
    .then(data=>{if(!Array.isArray(data)||!data.length)return;homepage(data);library(data);})
    .catch(error=>console.warn("Portfolio API unavailable; using static project content.",error));
})();