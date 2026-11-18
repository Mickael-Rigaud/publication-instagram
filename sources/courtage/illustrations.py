"""Illustrations vectorielles (aplats + faces d'ombre), viewBox 0 0 440 380, sol en bas."""

def svg(c):
    return f'<svg viewBox="0 0 440 380" xmlns="http://www.w3.org/2000/svg">{c}</svg>'

SOL = '<ellipse cx="220" cy="352" rx="175" ry="17" fill="#000" opacity=".12"/>'

def badge(x, y, r=44):
    return (f'<circle cx="{x+3}" cy="{y+5}" r="{r}" fill="#C9600C"/><circle cx="{x}" cy="{y}" r="{r}" fill="#F4801C"/>'
            f'<path d="M{x-r*.45} {y} l{r*.3} {r*.3} {r*.6} -{r*.62}" fill="none" stroke="#fff" stroke-width="{r*.24}" stroke-linecap="round" stroke-linejoin="round"/>')

def pieces(x, y, n=3):
    s = f'<g transform="translate({x},{y})"><rect x="0" y="{60-n*14}" width="84" height="{n*14}" fill="#E5980F"/><ellipse cx="42" cy="60" rx="42" ry="13" fill="#E5980F"/>'
    for i in range(n):
        s += f'<ellipse cx="42" cy="{60-i*14-14}" rx="42" ry="13" fill="{"#FFC44D" if i==n-1 else "#F4A21C"}"/>'
    return s + f'<ellipse cx="42" cy="{60-n*14}" rx="24" ry="6" fill="none" stroke="#F4A21C" stroke-width="4"/></g>'

def lignes(x, y, w, n, pas=26, c="#C9DDE8"):
    return "".join(f'<rect x="{x}" y="{y+i*pas}" width="{w if i%3!=2 else w*.6}" height="11" rx="5.5" fill="{c}"/>' for i in range(n))

def doc(x, y, w, h, contenu="", ombre=True):
    o = f'<rect x="{x+14}" y="{y+14}" width="{w}" height="{h}" rx="14" fill="#BFD6E2"/>' if ombre else ""
    return o + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#fff"/>' + contenu

BANQUE = svg(SOL + """
<rect x="58" y="300" width="324" height="40" rx="6" fill="#BFD6E2"/><rect x="58" y="300" width="324" height="12" rx="4" fill="#D9E8F0"/>
<rect x="82" y="276" width="276" height="28" rx="5" fill="#E7F1F6"/><rect x="82" y="296" width="276" height="8" fill="#C9DDE8"/>
<rect x="108" y="142" width="34" height="136" fill="#fff"/><rect x="130" y="142" width="12" height="136" fill="#D3E3EC"/>
<rect x="176" y="142" width="34" height="136" fill="#fff"/><rect x="198" y="142" width="12" height="136" fill="#D3E3EC"/>
<rect x="244" y="142" width="34" height="136" fill="#fff"/><rect x="266" y="142" width="12" height="136" fill="#D3E3EC"/>
<rect x="312" y="142" width="34" height="136" fill="#fff"/><rect x="334" y="142" width="12" height="136" fill="#D3E3EC"/>
<rect x="100" y="132" width="250" height="14" fill="#E7F1F6"/>
<rect x="82" y="104" width="276" height="30" rx="4" fill="#1D5B78"/><rect x="82" y="126" width="276" height="8" fill="#15384E"/>
<path d="M70 106 L220 34 L370 106 Z" fill="#15384E"/><path d="M120 98 L220 52 L320 98 Z" fill="#2A7FA6"/>
<circle cx="220" cy="82" r="12" fill="#FFC44D"/>""" + badge(362, 96, 50))

CAMEMBERT = svg(SOL + """<g transform="translate(10,22)"><path d="M190 190 L321.4 278.2 A150 150 0 1 1 190 40 Z" transform="translate(-10,0)" fill="#2A7FA6"/>
<path d="M216 172 L216 22 A150 150 0 0 1 337.4 260.2 Z" fill="#C9600C"/></g>
<g transform="translate(10,0)"><path d="M180 190 L311.4 278.2 A150 150 0 1 1 180 40 Z" fill="#4FB3D6"/>
<path d="M150 70 A120 120 0 0 0 80 150" fill="none" stroke="#7FCFE8" stroke-width="10" stroke-linecap="round"/>
<path d="M206 172 L206 22 A150 150 0 0 1 327.4 260.2 Z" fill="#F4801C"/>
<text x="262" y="150" font-family="Arial" font-weight="700" font-size="46" fill="#fff" text-anchor="middle">35%</text></g>""" + pieces(336, 270, 4))

CALENDRIER = svg(SOL + """
<rect x="96" y="70" width="264" height="270" rx="26" fill="#BFD6E2"/>
<rect x="82" y="58" width="264" height="270" rx="26" fill="#fff"/>
<path d="M82 84 a26 26 0 0 1 26 -26 h212 a26 26 0 0 1 26 26 v52 h-264z" fill="#F4801C"/>
<rect x="82" y="120" width="264" height="16" fill="#E5700F"/>
<rect x="134" y="36" width="20" height="54" rx="10" fill="#15384E"/><rect x="274" y="36" width="20" height="54" rx="10" fill="#15384E"/>
<text x="214" y="262" font-family="Arial" font-weight="700" font-size="120" fill="#1D5B78" text-anchor="middle">25</text>
<text x="214" y="306" font-family="Arial" font-weight="700" font-size="34" fill="#4FB3D6" text-anchor="middle">ANS</text>
<circle cx="350" cy="280" r="58" fill="#2A7FA6"/><circle cx="346" cy="274" r="58" fill="#4FB3D6"/><circle cx="346" cy="274" r="44" fill="#fff"/>
<path d="M346 246 v30 l20 12" fill="none" stroke="#15384E" stroke-width="9" stroke-linecap="round"/>""")

TIRELIRE = svg(SOL + """
<rect x="138" y="270" width="34" height="62" rx="10" fill="#2A7FA6"/><rect x="262" y="270" width="34" height="62" rx="10" fill="#2A7FA6"/>
<ellipse cx="216" cy="222" rx="140" ry="108" fill="#2A7FA6"/><ellipse cx="210" cy="214" rx="140" ry="106" fill="#4FB3D6"/>
<path d="M120 150 q30 -40 80 -46" fill="none" stroke="#7FCFE8" stroke-width="12" stroke-linecap="round"/>
<path d="M150 128 l-6 -62 l52 40z" fill="#2A7FA6"/>
<ellipse cx="340" cy="222" rx="34" ry="40" fill="#2A7FA6"/><ellipse cx="336" cy="220" rx="32" ry="38" fill="#7FCFE8"/>
<circle cx="328" cy="210" r="6" fill="#15384E"/><circle cx="344" cy="230" r="6" fill="#15384E"/>
<circle cx="290" cy="170" r="10" fill="#15384E"/>
<path d="M72 222 q-30 -6 -24 -36" fill="none" stroke="#4FB3D6" stroke-width="10" stroke-linecap="round"/>
<rect x="178" y="108" width="84" height="14" rx="7" fill="#15384E"/>
<ellipse cx="220" cy="62" rx="44" ry="44" fill="#E5980F"/><ellipse cx="216" cy="58" rx="44" ry="44" fill="#FFC44D"/>
<text x="216" y="76" font-family="Arial" font-weight="700" font-size="52" fill="#E5980F" text-anchor="middle">€</text>""")

PORTEFEUILLE = svg(SOL + """
<rect x="120" y="70" width="190" height="110" rx="10" fill="#7FCFE8" transform="rotate(-12 215 125)"/>
<rect x="150" y="60" width="190" height="110" rx="10" fill="#B9E6F3" transform="rotate(6 245 115)"/>
<text x="250" y="138" font-family="Arial" font-weight="700" font-size="60" fill="#4FB3D6" text-anchor="middle" transform="rotate(6 245 115)">€</text>
<rect x="72" y="140" width="300" height="196" rx="30" fill="#0F2C3E"/>
<rect x="66" y="128" width="300" height="196" rx="30" fill="#1D5B78"/>
<path d="M66 170 h300" stroke="#15384E" stroke-width="10"/>
<path d="M276 196 h104 a14 14 0 0 1 14 14 v50 a14 14 0 0 1 -14 14 h-104 a38 38 0 0 1 0 -78z" fill="#15384E"/>
<circle cx="286" cy="235" r="15" fill="#F4801C"/>""" + pieces(40, 270, 3))

MALLETTE = svg(SOL + """
<path d="M170 110 v-28 a18 18 0 0 1 18 -18 h64 a18 18 0 0 1 18 18 v28" fill="none" stroke="#15384E" stroke-width="18"/>
<rect x="74" y="118" width="304" height="216" rx="28" fill="#C9600C"/>
<rect x="64" y="106" width="304" height="216" rx="28" fill="#F4801C"/>
<path d="M64 196 h304" stroke="#E5700F" stroke-width="14"/>
<rect x="188" y="176" width="56" height="48" rx="10" fill="#15384E"/><rect x="204" y="190" width="24" height="12" rx="4" fill="#FFC44D"/>
<path d="M100 140 q20 -14 60 -14" fill="none" stroke="#F9A54A" stroke-width="10" stroke-linecap="round"/>
<rect x="352" y="250" width="40" height="84" rx="6" fill="#1D5B78"/>
<path d="M372 250 c-40 -30 -30 -80 0 -110 c30 30 40 80 0 110z" fill="#3E9B6B"/><path d="M372 250 v-100" stroke="#2E7A52" stroke-width="5"/>""")

def _graph(x, y):
    return (f'<rect x="{x}" y="{y+70}" width="28" height="40" rx="5" fill="#7FCFE8"/><rect x="{x+42}" y="{y+44}" width="28" height="66" rx="5" fill="#4FB3D6"/>'
            f'<rect x="{x+84}" y="{y+20}" width="28" height="90" rx="5" fill="#2A7FA6"/>'
            f'<path d="M{x-6} {y+60} L{x+50} {y+24} L{x+82} {y+38} L{x+130} {y-6}" fill="none" stroke="#F4801C" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')

RELEVE = svg(SOL + doc(110, 40, 210, 290, f'<rect x="110" y="40" width="210" height="56" rx="14" fill="#1D5B78"/><rect x="110" y="80" width="210" height="16" fill="#1D5B78"/>'
    + '<rect x="134" y="60" width="90" height="14" rx="7" fill="#7FCFE8"/>' + _graph(140, 130) + lignes(140, 272, 150, 2, 24)) + """
<circle cx="330" cy="250" r="52" fill="none" stroke="#15384E" stroke-width="16"/><circle cx="330" cy="250" r="44" fill="#D9F1F8" opacity=".8"/>
<path d="M368 290 l40 42" stroke="#15384E" stroke-width="22" stroke-linecap="round"/>""")

RELEVES = svg(SOL + '<g transform="rotate(-10 200 200)">' + doc(70, 70, 190, 250, lignes(96, 120, 130, 6), ombre=False) + '</g>'
    + '<g transform="rotate(5 260 200)">' + doc(150, 50, 200, 270, '<rect x="150" y="50" width="200" height="50" rx="14" fill="#4FB3D6"/>' + lignes(176, 130, 140, 6)) + '</g>'
    + '<g transform="rotate(-2 260 220)">' + doc(196, 96, 196, 240, '<rect x="196" y="96" width="196" height="50" rx="14" fill="#1D5B78"/>' + _graph(226, 170) + lignes(226, 300, 120, 1)) + '</g>')

BOUCLIER_MAISON = svg(SOL + """
<path d="M226 30 l136 46 v92 c0 90 -60 150 -136 182 c-76 -32 -136 -92 -136 -182 v-92z" fill="#2A7FA6"/>
<path d="M216 24 l136 46 v92 c0 90 -60 150 -136 182 c-76 -32 -136 -92 -136 -182 v-92z" fill="#4FB3D6"/>
<path d="M216 24 v320 c-76 -32 -136 -92 -136 -182 v-92z" fill="#7FCFE8" opacity=".45"/>
<path d="M146 190 l70 -58 l70 58" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M164 180 v74 h104 v-74" fill="#fff"/><rect x="200" y="210" width="32" height="44" rx="4" fill="#1D5B78"/>""" + badge(346, 250, 48))

ECHANGE = svg(SOL + '<g transform="rotate(-8 140 190)">' + doc(60, 90, 150, 200, '<rect x="60" y="90" width="150" height="44" rx="14" fill="#7FCFE8"/>' + lignes(82, 160, 100, 4)) + '</g>'
    + '<g transform="rotate(6 300 190)">' + doc(232, 80, 150, 200, '<rect x="232" y="80" width="150" height="44" rx="14" fill="#F4801C"/>' + lignes(254, 150, 100, 4)) + '</g>' + """
<path d="M150 70 q70 -60 140 -6" fill="none" stroke="#F4801C" stroke-width="12" stroke-linecap="round"/><path d="M276 40 l20 26 l-32 6z" fill="#F4801C"/>
<path d="M300 320 q-70 50 -150 6" fill="none" stroke="#F4801C" stroke-width="12" stroke-linecap="round"/><path d="M164 350 l-22 -26 l32 -4z" fill="#F4801C"/>""")

def _bouclier(x, s, c1, c2):
    return (f'<g transform="translate({x},60) scale({s})"><path d="M90 6 l84 28 v58 c0 58 -38 96 -84 116 c-46 -20 -84 -58 -84 -116 v-58z" fill="{c2}" transform="translate(6,6)"/>'
            f'<path d="M90 6 l84 28 v58 c0 58 -38 96 -84 116 c-46 -20 -84 -58 -84 -116 v-58z" fill="{c1}"/>'
            f'<path d="M58 100 l22 22 l42 -46" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></g>')
EQUIVALENT = svg(SOL + _bouclier(20, 1, "#4FB3D6", "#2A7FA6") + _bouclier(240, 1, "#F4801C", "#C9600C")
    + '<rect x="196" y="142" width="48" height="13" rx="6" fill="#FFFFFF"/><rect x="196" y="170" width="48" height="13" rx="6" fill="#FFFFFF"/>')

SANTE = svg(SOL + """<rect x="104" y="58" width="236" height="290" rx="24" fill="#C9600C"/><rect x="92" y="46" width="236" height="290" rx="24" fill="#F4801C"/>
<rect x="114" y="74" width="192" height="244" rx="12" fill="#fff"/>
<rect x="160" y="28" width="100" height="44" rx="12" fill="#15384E"/>
<path d="M210 156 c-30 -30 -62 0 -40 26 l40 38 l40 -38 c22 -26 -10 -56 -40 -26z" fill="#4FB3D6"/>""" + lignes(146, 236, 128, 3, 24)
    + '<g transform="translate(316 252)"><circle r="56" fill="#2A7FA6"/><circle r="56" fill="#4FB3D6" transform="translate(-4 -4)"/>'
      '<path d="M-24 -24 L20 20 M20 -24 L-24 20" stroke="#fff" stroke-width="14" stroke-linecap="round"/></g>')

DOSSIER = svg(SOL + """<path d="M70 110 a18 18 0 0 1 18 -18 h82 l24 26 h158 a18 18 0 0 1 18 18 v190 a18 18 0 0 1 -18 18 h-264 a18 18 0 0 1 -18 -18z" fill="#15384E"/>"""
    + '<g transform="rotate(-6 200 150)">' + doc(110, 60, 170, 200, lignes(132, 96, 120, 5), ombre=False) + '</g>'
    + '<g transform="rotate(5 260 150)">' + doc(190, 70, 170, 200, '<rect x="190" y="70" width="170" height="40" rx="14" fill="#4FB3D6"/>' + lignes(212, 132, 120, 4), ombre=False) + '</g>'
    + """<path d="M60 172 a18 18 0 0 1 18 -18 h290 a18 18 0 0 1 18 18 l-14 150 a18 18 0 0 1 -18 16 h-262 a18 18 0 0 1 -18 -16z" fill="#1D5B78"/>
<path d="M90 190 h120" stroke="#2A7FA6" stroke-width="10" stroke-linecap="round"/>""" + badge(352, 150, 46))

IDENTITE = svg(SOL + """<rect x="68" y="92" width="320" height="214" rx="26" fill="#BFD6E2"/><rect x="54" y="78" width="320" height="214" rx="26" fill="#fff"/>
<path d="M54 104 a26 26 0 0 1 26 -26 h268 a26 26 0 0 1 26 26 v20 h-320z" fill="#1D5B78"/>
<rect x="84" y="150" width="100" height="116" rx="14" fill="#D9F1F8"/><circle cx="134" cy="194" r="24" fill="#4FB3D6"/>
<path d="M98 260 c4 -34 68 -34 72 0z" fill="#4FB3D6"/>""" + lignes(208, 160, 140, 4, 28) + """
<rect x="250" y="40" width="130" height="60" rx="14" fill="#F4801C" transform="rotate(8 315 70)"/>
<circle cx="296" cy="72" r="10" fill="#fff" transform="rotate(8 315 70)"/><rect x="314" y="64" width="50" height="10" rx="5" fill="#fff" transform="rotate(8 315 70)"/>""")

BULLETIN = svg(SOL + doc(100, 36, 220, 296, '<rect x="100" y="36" width="220" height="54" rx="14" fill="#4FB3D6"/><rect x="100" y="72" width="220" height="18" fill="#4FB3D6"/>'
    + '<rect x="122" y="54" width="110" height="14" rx="7" fill="#fff"/>' + lignes(124, 116, 170, 6, 26)
    + '<rect x="124" y="276" width="172" height="34" rx="8" fill="#FDE6CF"/><rect x="236" y="285" width="50" height="16" rx="8" fill="#F4801C"/>')
    + '<ellipse cx="338" cy="250" rx="62" ry="62" fill="#E5980F"/><ellipse cx="332" cy="244" rx="62" ry="62" fill="#FFC44D"/>'
      '<ellipse cx="332" cy="244" rx="46" ry="46" fill="none" stroke="#F4A21C" stroke-width="6"/>'
      '<text x="332" y="266" font-family="Arial" font-weight="700" font-size="62" fill="#E5980F" text-anchor="middle">€</text>')

MAISON_CLE = svg(SOL + """
<rect x="96" y="170" width="236" height="166" fill="#E7F1F6"/><rect x="290" y="170" width="42" height="166" fill="#C9DDE8"/>
<path d="M70 184 L214 70 L358 184" fill="none" stroke="#F4801C" stroke-width="34" stroke-linejoin="round" stroke-linecap="round"/>
<rect x="282" y="72" width="30" height="70" fill="#1D5B78"/>
<rect x="128" y="206" width="56" height="52" rx="6" fill="#4FB3D6"/><path d="M156 206 v52 M128 232 h56" stroke="#fff" stroke-width="5"/>
<rect x="210" y="236" width="56" height="100" rx="6" fill="#1D5B78"/><circle cx="254" cy="290" r="5" fill="#FFC44D"/>
<g transform="translate(350 236) rotate(-35)"><circle r="34" fill="#E5980F"/><circle r="34" fill="#FFC44D" transform="translate(-3 -3)"/><circle r="12" fill="#FFF3E2" transform="translate(-3 -3)"/>
<rect x="26" y="-10" width="90" height="18" rx="5" fill="#FFC44D"/><rect x="92" y="6" width="12" height="20" fill="#FFC44D"/><rect x="70" y="6" width="12" height="14" fill="#FFC44D"/></g>
<path d="M60 336 c-20 -40 0 -90 26 -100 c24 22 30 70 -6 100z" fill="#3E9B6B"/>""")

CONTRAT = svg(SOL + doc(96, 34, 230, 300, '<rect x="122" y="64" width="120" height="16" rx="8" fill="#1D5B78"/>' + lignes(122, 108, 176, 6, 26)
    + '<path d="M130 290 c20 -30 34 10 50 -12 s30 8 44 -6" fill="none" stroke="#2A7FA6" stroke-width="6" stroke-linecap="round"/><rect x="122" y="300" width="130" height="5" rx="2" fill="#C9DDE8"/>')
    + pieces(306, 250, 3) + badge(330, 110, 52)
    + '<text x="210" y="264" font-family="Arial" font-weight="700" font-size="54" fill="#F4801C" text-anchor="middle" opacity=".9">0 €</text>')
