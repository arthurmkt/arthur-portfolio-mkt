"""Renderiza uma peça de motion (HTML do template) quadro a quadro e gera o MP4.

Uso:
  python render.py peca.html                         -> peca.mp4 (vídeo inteiro)
  python render.py peca.html --segments 0-3,11-15 -o peca_6s.mp4   (versão curta: junta trechos)
  python render.py peca.html --sheet 1.5,5,9,13 -o revisao.png     (folha de revisão com quadros nesses segundos)
  python render.py peca.html --sheet auto --safe                   (meio e fim de cada cena, com área segura)
  python render.py peca.html --audio trilha.mp3                    (mixa trilha licenciada; corta no fim do vídeo)

Por que servidor local e não file://: imagem carregada de file:// "suja" o canvas e
quebra técnica que lê pixels (partículas formando logo). E fonte local carrega igual.
"""
import argparse, http.server, functools, threading, socketserver, subprocess, pathlib, shutil, sys, io, json


def servir(pasta):
    class Quieto(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k):
            pass
    h = functools.partial(Quieto, directory=str(pasta))
    srv = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


def abrir(pw, url, W, H):
    b = pw.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    pg.goto(url, wait_until="networkidle")
    pg.evaluate("window.__ready")
    return b, pg


def quadro(pg, t, W, H, safe=False):
    if safe:
        pg.evaluate("document.getElementById('safe').checked=true; document.getElementById('safe').dispatchEvent(new Event('change'))")
    pg.evaluate(f"window.__render({t:.6f})")
    return pg.screenshot(type="png", clip={"x": 0, "y": 0, "width": W, "height": H})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("-o", "--out")
    ap.add_argument("--segments", help="trechos em segundos, ex: 0-3,11-15")
    ap.add_argument("--sheet", help="segundos separados por vírgula, ou 'auto'")
    ap.add_argument("--safe", action="store_true", help="na folha de revisão, pinta a área segura")
    ap.add_argument("--audio")
    ap.add_argument("--crf", default="18")
    a = ap.parse_args()

    html = pathlib.Path(a.html).resolve()
    srv, port = servir(html.parent)
    url = f"http://127.0.0.1:{port}/{html.name}?render=1"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        # lê o formato da própria peça
        b0 = pw.chromium.launch(channel="chrome"); p0 = b0.new_page(); p0.goto(url, wait_until="networkidle")
        cfg = p0.evaluate("(() => ({W: CFG.W, H: CFG.H, FPS: CFG.FPS, DUR: CFG.DUR}))()")
        cenas = p0.evaluate("SCENES.map(s => [s.name, s.start, s.end])")
        b0.close()
        W, H, FPS, DUR = cfg["W"], cfg["H"], cfg["FPS"], cfg["DUR"]
        b, pg = abrir(pw, url, W, H)

        if a.sheet:
            from PIL import Image, ImageDraw
            if a.sheet == "auto":
                ts = []
                for _, s, e in cenas:
                    ts += [round((s + e) / 2, 3), round(max(s, e - 0.05), 3)]
            else:
                ts = [float(x) for x in a.sheet.split(",")]
            esc = 360 / W
            tw, th = int(W * esc), int(H * esc)
            cols = min(4, len(ts)); rows = (len(ts) + cols - 1) // cols
            folha = Image.new("RGB", (cols * (tw + 12) + 12, rows * (th + 40) + 12), "#1a1a1a")
            d = ImageDraw.Draw(folha)
            try:
                from PIL import ImageFont
                fonte = ImageFont.truetype("arial.ttf", 15)
            except OSError:
                fonte = None
            for i, t in enumerate(ts):
                im = Image.open(io.BytesIO(quadro(pg, t, W, H, a.safe))).convert("RGB").resize((tw, th), Image.LANCZOS)
                x, y = 12 + (i % cols) * (tw + 12), 12 + (i // cols) * (th + 40)
                folha.paste(im, (x, y + 28))
                nome = next((n for n, s, e in cenas if s <= t < e or (t == e == DUR)), "")
                d.text((x, y + 6), f"{t:.2f}s  {nome}"[:60], fill="#fff", font=fonte)
            out = pathlib.Path(a.out or html.with_name(html.stem + "_revisao.png"))
            folha.save(out)
            print(f"folha: {out}  ({len(ts)} quadros)")
            b.close(); srv.shutdown(); return

        ff = shutil.which("ffmpeg")
        if not ff:
            sys.exit("ffmpeg não encontrado no PATH")
        trechos = [(0.0, float(DUR))]
        if a.segments:
            trechos = [tuple(map(float, s.split("-"))) for s in a.segments.split(",")]
        out = pathlib.Path(a.out or html.with_suffix(".mp4"))
        cmd = [ff, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-"]
        if a.audio:
            cmd += ["-i", a.audio, "-c:a", "aac", "-b:a", "192k", "-shortest"]
        cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", a.crf, "-preset", "medium", "-movflags", "+faststart", str(out)]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        total = 0
        for ini, fim in trechos:
            n = round((fim - ini) * FPS)
            for i in range(n):
                proc.stdin.write(quadro(pg, ini + i / FPS, W, H))
                total += 1
                if total % FPS == 0:
                    print(f"\r{total} quadros", end="", flush=True)
        proc.stdin.close(); proc.wait()
        b.close(); srv.shutdown()
        print(f"\nMP4: {out}  {W}x{H} {FPS}fps  {total} quadros = {total / FPS:.2f}s")


if __name__ == "__main__":
    main()
