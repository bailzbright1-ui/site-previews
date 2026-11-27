BANNER = '<!--PREVIEW--><div style="position:relative;z-index:100;background:#111;color:#eee;font:500 13px/1.45 system-ui,sans-serif;text-align:center;padding:9px 16px">Website concept for {{NAME}}, made by {{AGENCY}}. Preview only &middot; not the official site yet.</div><!--/PREVIEW-->'
NOINDEX = '<meta name="robots" content="noindex, nofollow"><!-- PREVIEW-ONLY -->'
FORMJS = r"""<script>
document.querySelectorAll('form[data-lead]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();if(!f.checkValidity()){f.reportValidity();return}var ep='{{FORM_ENDPOINT}}',b=f.querySelector('[type=submit]');if(!ep){f.classList.add('sent');return}b.disabled=true;b.textContent='Sending…';fetch(ep,{method:'POST',headers:{Accept:'application/json'},body:new FormData(f)}).then(function(r){if(!r.ok)throw 0;f.classList.add('sent')}).catch(function(){b.disabled=false;b.textContent='Try again';alert('Sorry, that did not send. Please call us instead.')})})});
</script>"""
PVNOTE = '<!--PREVIEW--><p style="font-size:13px;opacity:.7;margin-top:10px">Preview: once live, this goes straight to {{NAME}}\'s inbox.</p><!--/PREVIEW-->'
