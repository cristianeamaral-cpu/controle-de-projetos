"""Gera faq.md, faq.html e faq-schema.jsonld a partir de faq.json.

Uso: python3 docs/faq-ecossistema-palestrantes/gerar.py
"""
import html
import json
import re
from pathlib import Path

PASTA = Path(__file__).resolve().parent


def inline_html(texto):
    texto = html.escape(texto, quote=False)
    texto = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', texto)
    texto = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", texto)
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", texto)


def resposta_html(md):
    partes = []
    for bloco in md.split("\n\n"):
        linhas = bloco.split("\n")
        if all(l.startswith("- ") for l in linhas):
            itens = "".join(f"<li>{inline_html(l[2:])}</li>" for l in linhas)
            partes.append(f"<ul>{itens}</ul>")
        elif all(re.match(r"\d+\. ", l) for l in linhas):
            itens = "".join(f"<li>{inline_html(l.split('. ', 1)[1])}</li>" for l in linhas)
            partes.append(f"<ol>{itens}</ol>")
        else:
            partes.append(f"<p>{inline_html(bloco)}</p>")
    return "".join(partes)


def perguntas(faq):
    for secao in faq["secoes"]:
        for sub in secao["subsecoes"]:
            for p in sub["perguntas"]:
                yield secao, sub, p


def gerar_md(faq):
    out = [f"# {faq['titulo']}", "", f"_Versão {faq['versao']} · atualizado em {faq['atualizado_em']}_", ""]
    for secao in faq["secoes"]:
        out += [f"## {secao['ordem']:02d}. {secao['titulo']}", ""]
        for sub in secao["subsecoes"]:
            if sub["titulo"]:
                out += [f"### {sub['titulo']}", ""]
            for p in sub["perguntas"]:
                out += [f"**{p['pergunta']}**", "", p["resposta"], ""]
    return "\n".join(out)


def gerar_html(faq):
    out = [f'<section class="psa-faq" lang="{faq["idioma"]}">', f"  <h1>{html.escape(faq['titulo'])}</h1>"]
    for secao in faq["secoes"]:
        out.append(f'  <h2 id="{secao["id"]}">{secao["ordem"]:02d}. {html.escape(secao["titulo"])}</h2>')
        for sub in secao["subsecoes"]:
            if sub["titulo"]:
                out.append(f'  <h3 id="{sub["id"]}">{html.escape(sub["titulo"])}</h3>')
            for p in sub["perguntas"]:
                out += [
                    f'  <details id="{p["id"]}">',
                    f"    <summary>{html.escape(p['pergunta'])}</summary>",
                    f"    <div>{resposta_html(p['resposta'])}</div>",
                    "  </details>",
                ]
    out.append("</section>")
    return "\n".join(out) + "\n"


def gerar_jsonld(faq):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": faq["idioma"],
        "mainEntity": [
            {
                "@type": "Question",
                "name": p["pergunta"],
                "acceptedAnswer": {"@type": "Answer", "text": resposta_html(p["resposta"])},
            }
            for _, _, p in perguntas(faq)
        ],
    }


def main():
    faq = json.loads((PASTA / "faq.json").read_text(encoding="utf-8"))
    ids = [p["id"] for _, _, p in perguntas(faq)]
    assert len(ids) == len(set(ids)), "IDs de perguntas repetidos"
    (PASTA / "faq.md").write_text(gerar_md(faq), encoding="utf-8")
    (PASTA / "faq.html").write_text(gerar_html(faq), encoding="utf-8")
    (PASTA / "faq-schema.jsonld").write_text(
        json.dumps(gerar_jsonld(faq), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{len(ids)} perguntas geradas")


if __name__ == "__main__":
    main()
