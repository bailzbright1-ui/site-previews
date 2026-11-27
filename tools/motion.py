# Shared motion layer injected into every site by build.py.
# Mark elements with: data-r (fade+rise) | data-r="left" | data-r="scale" | data-r="clip" (image curtain)
# optional data-d="120" (delay ms) · data-px="0.12" parallax (on images/blocks) · data-count="41" counters
HEAD = """<script>document.documentElement.classList.add('js')</script>
<style>
html.js [data-r]{opacity:0;transform:translateY(28px);transition:opacity .8s cubic-bezier(.2,.7,.2,1),transform .9s cubic-bezier(.2,.7,.2,1)}
html.js [data-r=left]{transform:translateX(-36px)}
html.js [data-r=scale]{transform:scale(.94)}
html.js [data-r=clip]{opacity:1;transform:none}
html.js [data-r=clip]>*{clip-path:inset(100% 0 0 0);transition:clip-path 1.1s cubic-bezier(.7,0,.2,1)}
html.js [data-r].in{opacity:1;transform:none}
html.js [data-r=clip].in>*{clip-path:inset(0 0 0 0)}
[data-px]{will-change:transform}
.zoom{overflow:hidden}.zoom img{transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}.zoom:hover img{transform:scale(1.05)}
@media (prefers-reduced-motion:reduce){html.js [data-r],html.js [data-r]>*{opacity:1!important;transform:none!important;clip-path:none!important;transition:none!important}[data-px]{transform:none!important}}
</style>"""
BODY = """<script>
(function(){var rm=matchMedia('(prefers-reduced-motion: reduce)').matches,els=[].slice.call(document.querySelectorAll('[data-r]'));
function show(e){e.classList.add('in')}
if(rm||!('IntersectionObserver' in window)){els.forEach(show)}else{var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){var e=x.target;setTimeout(function(){show(e)},+(e.dataset.d||0));io.unobserve(e)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});els.forEach(function(e){io.observe(e)})}
function sweep(){els.forEach(function(e){if(!e.classList.contains('in')&&e.getBoundingClientRect().top<innerHeight*.94)show(e)})}addEventListener('scroll',function(){requestAnimationFrame(sweep)},{passive:true});addEventListener('hashchange',sweep);setTimeout(sweep,300);setTimeout(function(){els.forEach(show)},6000);
var px=[].slice.call(document.querySelectorAll('[data-px]'));
if(!rm&&px.length){var t=false;function upd(){px.forEach(function(e){var r=e.getBoundingClientRect(),c=r.top+r.height/2-innerHeight/2;e.style.transform='translate3d(0,'+(c*-(+e.dataset.px)).toFixed(1)+'px,0)'});t=false}addEventListener('scroll',function(){if(!t){t=true;requestAnimationFrame(upd)}},{passive:true});upd()}
var cs=[].slice.call(document.querySelectorAll('[data-count]'));
if(cs.length&&!rm&&'IntersectionObserver' in window){var co=new IntersectionObserver(function(es){es.forEach(function(x){if(!x.isIntersecting)return;co.unobserve(x.target);var e=x.target,to=+e.dataset.count,fr=+(e.dataset.from||0),t0=performance.now();(function s(n){var p=Math.min(1,(n-t0)/1500);e.textContent=Math.round(fr+(to-fr)*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(s)})(t0)})},{threshold:.5});cs.forEach(function(e){co.observe(e)})}
})();
</script>"""
