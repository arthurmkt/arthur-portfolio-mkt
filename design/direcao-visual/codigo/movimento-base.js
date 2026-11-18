/* Extraído de um site de agência no ar, out/2026.
   - split por palavra + reveal ao entrar na tela (IntersectionObserver)
   - números contando, parallax leve, nav que escurece ao rolar
   - marquee contínuo
   - fundo em fluxo: shader WebGL de ruído (família do gradiente da Stripe),
     só liga se houver WebGL e se a pessoa não pediu menos movimento.
   Ajustar os seletores (splitSel, groups) ao HTML novo. */

(function(){
  var root=document.documentElement; root.classList.add("js");
  var reduce=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var vh=function(){return window.innerHeight||document.documentElement.clientHeight};

  /* ---- split por palavra (equivalente ao SplitType + words-slide-up) ---- */
  function splitWords(node){
    Array.prototype.slice.call(node.childNodes).forEach(function(child){
      if(child.nodeType===3){
        var frag=document.createDocumentFragment();
        child.textContent.split(/(\s+)/).forEach(function(tok){
          if(!tok) return;
          if(/^\s+$/.test(tok)){ frag.appendChild(document.createTextNode(" ")); return; }
          var o=document.createElement("span"); o.className="w";
          var i=document.createElement("span"); i.className="wi"; i.textContent=tok;
          o.appendChild(i); frag.appendChild(o);
        });
        node.replaceChild(frag,child);
      } else if(child.nodeType===1 && child.tagName!=="BR"){ splitWords(child); }
    });
  }
  var splitSel=".sh h2, .num-head h2, .tl-head h2, .founder h2, .form-wrap h2, .foot-top h2, .anchor, .done h3";
  var groups=[".num",".cards .card",".compare .col",".step",".instruments",".founder",".form-side .filters div","form",".faq details",".foot-card",".num-head .lead",".sh .lead",".tl-head .lead",".form-wrap .lead",".tl-top"];
  var splits=Array.prototype.slice.call(document.querySelectorAll(splitSel));
  var reveals=[]; groups.forEach(function(sel){ document.querySelectorAll(sel).forEach(function(el,i){ reveals.push({el:el,i:i}); }); });

  /* Tudo que já aparece na primeira tela fica visível de imediato (sem animação de entrada):
     é o que deixa a página "pronta" mais rápido para o visitante e para o PageSpeed.
     As animações continuam em tudo que está abaixo da dobra.
     Primeiro só LEMOS as posições (um único cálculo de layout), depois escrevemos. */
  var H0=vh();
  function abaixo(el){ return !el.closest(".hero") && el.getBoundingClientRect().top>=H0; }
  var splitsAbaixo=reduce?[]:splits.filter(abaixo);
  var revealsAbaixo=reduce?[]:reveals.filter(function(o){ return abaixo(o.el); });
  var steps=document.querySelector(".steps"); var stepsAbaixo=steps&&!reduce&&abaixo(steps);

  splitsAbaixo.forEach(function(el){
    splitWords(el); el.classList.add("split","pre");
    var words=el.querySelectorAll(".wi"), n=Math.max(words.length-1,1);
    words.forEach(function(w,i){ w.style.transitionDelay=Math.round(i/n*500)+"ms"; });
  });
  revealsAbaixo.forEach(function(o){ o.el.classList.add("rv","pre"); o.el.style.transitionDelay=(o.i%8*90)+"ms"; });
  if(steps){ steps.classList.add(stepsAbaixo?"pre":"in"); }

  /* ---- observer: revela ao entrar na tela; rearma ao rolar de volta para cima ---- */
  var targets=splitsAbaixo.concat(revealsAbaixo.map(function(o){return o.el;})); if(stepsAbaixo) targets.push(steps);
  var counted=false;
  function reveal(el){ el.classList.remove("pre"); el.classList.add("in"); if(el.classList.contains("num")) countUp(); }
  function arm(el){ el.classList.remove("in"); el.classList.add("pre"); }
  if("IntersectionObserver" in window){
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){ reveal(e.target); }
        else if(e.boundingClientRect.top>vh()){ arm(e.target); }
      });
    },{threshold:0.12,rootMargin:"0px 0px -8% 0px"});
    targets.forEach(function(el){ io.observe(el); });
  } else { targets.forEach(reveal); }

  /* ---- números contando ---- */
  function countUp(){
    if(counted) return; counted=true;
    document.querySelectorAll(".cnt[data-count]").forEach(function(el){
      var to=parseInt(el.getAttribute("data-count"),10), t0=null, dur=1300;
      function f(t){ if(!t0) t0=t; var p=Math.min((t-t0)/dur,1), e=1-Math.pow(1-p,3); el.textContent=Math.round(to*e); if(p<1) requestAnimationFrame(f); }
      if(reduce){ el.textContent=to; } else requestAnimationFrame(f);
    });
  }

  /* ---- parallax leve nas imagens ---- */
  var px=Array.prototype.slice.call(document.querySelectorAll("[data-px]"));
  var heroWrap=document.querySelector(".hero .wrap");
  var ticking=false;
  function onScroll(){
    if(ticking) return; ticking=true;
    requestAnimationFrame(function(){
      var H=vh(), y=window.scrollY||0;
      px.forEach(function(el){
        var r=el.getBoundingClientRect(); if(r.bottom<0||r.top>H) return;
        var c=r.top+r.height/2-H/2, f=parseFloat(el.getAttribute("data-px"))||0;
        el.style.transform="translate3d(0,"+(c*f).toFixed(1)+"px,0)";
      });
      if(heroWrap && y<H){ heroWrap.style.transform="translate3d(0,"+(y*0.18).toFixed(1)+"px,0)"; heroWrap.style.opacity=String(Math.max(1-y/(H*0.9),0)); }
      var nav=document.querySelector(".nav"); if(nav) nav.classList.toggle("scrolled",y>40);
      ticking=false;
    });
  }
  if(!reduce){ window.addEventListener("scroll",onScroll,{passive:true}); window.addEventListener("resize",onScroll); onScroll(); }

  /* ---- marquee: duplica o conteúdo para o loop ficar contínuo ---- */
  var mq=document.getElementById("mq-track"); if(mq){ mq.innerHTML+=mq.innerHTML; }

  /* ---- fundo em fluxo: shader de ruído (mesma família do gradiente WebGL da Stripe) ---- */
  (function(){
    var cv=document.getElementById("flow-bg"); if(!cv||reduce) return;
    var iniciou=false; function iniciar(){ if(iniciou) return; iniciou=true;
    var gl=cv.getContext("webgl",{antialias:false,alpha:false,depth:false,stencil:false,powerPreference:"low-power"})||cv.getContext("experimental-webgl");
    if(!gl) return;
    var vs="attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}";
    var fs=[
      "precision highp float;",
      "uniform vec2 u_res;uniform float u_time;uniform vec3 u_c0,u_c1,u_c2,u_c3;",
      "vec3 mod289(vec3 x){return x-floor(x*(1.0/289.0))*289.0;}",
      "vec4 mod289(vec4 x){return x-floor(x*(1.0/289.0))*289.0;}",
      "vec4 permute(vec4 x){return mod289(((x*34.0)+1.0)*x);}",
      "vec4 taylorInvSqrt(vec4 r){return 1.79284291400159-0.85373472095314*r;}",
      "float snoise(vec3 v){const vec2 C=vec2(1.0/6.0,1.0/3.0);const vec4 D=vec4(0.0,0.5,1.0,2.0);",
      "vec3 i=floor(v+dot(v,C.yyy));vec3 x0=v-i+dot(i,C.xxx);vec3 g=step(x0.yzx,x0.xyz);vec3 l=1.0-g;",
      "vec3 i1=min(g.xyz,l.zxy);vec3 i2=max(g.xyz,l.zxy);vec3 x1=x0-i1+C.xxx;vec3 x2=x0-i2+C.yyy;vec3 x3=x0-D.yyy;",
      "i=mod289(i);vec4 p=permute(permute(permute(i.z+vec4(0.0,i1.z,i2.z,1.0))+i.y+vec4(0.0,i1.y,i2.y,1.0))+i.x+vec4(0.0,i1.x,i2.x,1.0));",
      "float n_=0.142857142857;vec3 ns=n_*D.wyz-D.xzx;vec4 j=p-49.0*floor(p*ns.z*ns.z);vec4 x_=floor(j*ns.z);vec4 y_=floor(j-7.0*x_);",
      "vec4 x=x_*ns.x+ns.yyyy;vec4 y=y_*ns.x+ns.yyyy;vec4 h=1.0-abs(x)-abs(y);vec4 b0=vec4(x.xy,y.xy);vec4 b1=vec4(x.zw,y.zw);",
      "vec4 s0=floor(b0)*2.0+1.0;vec4 s1=floor(b1)*2.0+1.0;vec4 sh=-step(h,vec4(0.0));vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy;vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;",
      "vec3 p0=vec3(a0.xy,h.x);vec3 p1=vec3(a0.zw,h.y);vec3 p2=vec3(a1.xy,h.z);vec3 p3=vec3(a1.zw,h.w);",
      "vec4 norm=taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));p0*=norm.x;p1*=norm.y;p2*=norm.z;p3*=norm.w;",
      "vec4 m=max(0.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.0);m=m*m;return 42.0*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));}",
      "void main(){",
      "vec2 uv=gl_FragCoord.xy/u_res;float asp=u_res.x/u_res.y;vec2 p=vec2(uv.x*asp,uv.y);float t=u_time;",
      /* ondulação vertical lenta (efeito de tecido) + fluxo horizontal contínuo = avanço */
      "float wave=snoise(vec3(p.x*0.9+t*0.10,p.y*1.5,t*0.07))*0.22;",
      "vec2 q=vec2(p.x-t*0.085,p.y+wave);",
      "vec3 col=u_c0;",
      "float n1=snoise(vec3(q.x*1.15,q.y*1.5+t*0.04,t*0.06))*0.5+0.5;col=mix(col,u_c1,smoothstep(0.34,0.78,n1));",
      "float n2=snoise(vec3(q.x*1.7+3.1,q.y*1.05,t*0.08+1.0))*0.5+0.5;col=mix(col,u_c2,smoothstep(0.46,0.86,n2));",
      "float n3=snoise(vec3(q.x*0.75+7.0,q.y*2.1+t*0.03,t*0.05+2.0))*0.5+0.5;col=mix(col,u_c3,smoothstep(0.56,0.92,n3)*0.95);",
      /* faixa de luz diagonal atravessando */
      "float band=fract((p.x*0.32-p.y*0.22)-t*0.045);float sweep=smoothstep(0.0,1.0,1.0-abs(band*2.0-1.0));sweep=pow(sweep,6.0);col+=sweep*0.045;",
      /* vinheta */
      "col*=1.0-0.28*length(uv-vec2(0.5,0.45));",
      "gl_FragColor=vec4(col,1.0);}"
    ].join("\n");
    function sh(type,src){var s=gl.createShader(type);gl.shaderSource(s,src);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)){return null;}return s;}
    var v=sh(gl.VERTEX_SHADER,vs), f=sh(gl.FRAGMENT_SHADER,fs); if(!v||!f) return;
    var pr=gl.createProgram();gl.attachShader(pr,v);gl.attachShader(pr,f);gl.linkProgram(pr);
    if(!gl.getProgramParameter(pr,gl.LINK_STATUS)) return;
    gl.useProgram(pr);
    var buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
    var a=gl.getAttribLocation(pr,"a");gl.enableVertexAttribArray(a);gl.vertexAttribPointer(a,2,gl.FLOAT,false,0,0);
    var uRes=gl.getUniformLocation(pr,"u_res"),uT=gl.getUniformLocation(pr,"u_time");
    function c(hex){return [(hex>>16&255)/255,(hex>>8&255)/255,(hex&255)/255];}
    /* paleta do fundo: troque pelos tokens do projeto */
    gl.uniform3fv(gl.getUniformLocation(pr,"u_c0"),c(0x0f1623));
    gl.uniform3fv(gl.getUniformLocation(pr,"u_c1"),c(0x3a4560));
    gl.uniform3fv(gl.getUniformLocation(pr,"u_c2"),c(0x1c2640));
    gl.uniform3fv(gl.getUniformLocation(pr,"u_c3"),c(0x6b2a14));
    var W=0,H=0;
    function resize(){var s=Math.min(window.devicePixelRatio||1,1.5)*0.42;W=Math.max(1,Math.floor(window.innerWidth*s));H=Math.max(1,Math.floor(window.innerHeight*s));cv.width=W;cv.height=H;gl.viewport(0,0,W,H);gl.uniform2f(uRes,W,H);}
    resize(); window.addEventListener("resize",resize);
    root.classList.add("gl");
    var running=true,t0=performance.now();
    function frame(now){ if(!running) return; gl.uniform1f(uT,(now-t0)/1000); gl.drawArrays(gl.TRIANGLES,0,3); requestAnimationFrame(frame); }
    requestAnimationFrame(frame);
    document.addEventListener("visibilitychange",function(){var was=running;running=!document.hidden;if(running&&!was) requestAnimationFrame(frame);});
    }
    /* o fundo só liga na primeira interação: dispare window.dispatchEvent(new Event("site:interagiu"))
       no primeiro scroll/toque (o mesmo gatilho que carrega o GTM). */
    window.addEventListener("site:interagiu",iniciar,{once:true});
  })();
})();
