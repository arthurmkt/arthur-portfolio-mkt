
/* Rolagem ate ancora com duracao fixa.
   O scroll-behavior nativo anima a distancia inteira: numa pagina longa,
   ir do rodape ao formulario passa de 1 segundo. Aqui perto e longe levam
   o mesmo tempo, e o alvo para abaixo da barra fixa em vez de atras dela. */
(function(){
  var DURACAO = 480;
  var menos = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function irPara(alvo, hash){
    var nav = document.querySelector(".nav");
    var folga = (nav ? nav.offsetHeight : 0) + 8;
    var de = window.pageYOffset;
    var para = Math.max(0, alvo.getBoundingClientRect().top + de - folga);
    function fim(){ try{ history.replaceState(null, "", hash); }catch(e){} }
    if(menos || Math.abs(para - de) < 4){ window.scrollTo(0, para); fim(); return; }
    var t0 = performance.now();
    requestAnimationFrame(function passo(agora){
      var p = Math.min((agora - t0) / DURACAO, 1);
      var e = p < 0.5 ? 4*p*p*p : 1 - Math.pow(-2*p + 2, 3) / 2;
      window.scrollTo(0, de + (para - de) * e);
      if(p < 1) requestAnimationFrame(passo); else fim();
    });
  }

  document.addEventListener("click", function(ev){
    if(ev.defaultPrevented || ev.button !== 0 || ev.metaKey || ev.ctrlKey || ev.shiftKey) return;
    var a = ev.target.closest('a[href^="#"]');
    if(!a) return;
    var hash = a.getAttribute("href");
    if(!hash || hash === "#") return;
    var alvo = document.getElementById(hash.slice(1));
    if(!alvo) return;
    ev.preventDefault();
    irPara(alvo, hash);
  }, {passive:false});
})();
