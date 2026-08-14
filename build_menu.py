#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""menu_data.py 를 읽어 menu.html 을 생성한다.

    python3 build_menu.py

가격을 고치려면 menu_data.py 만 손보고 다시 실행하면 된다.
"""

import html
import re
from pathlib import Path

import menu_data as D

OUT = Path(__file__).parent / "menu.html"


def e(s):
    return html.escape(str(s), quote=True)


def won(n):
    """18 → '18,000'. 메뉴 원본의 '18.' 표기를 원 단위로 편다."""
    return f"{n * 1000:,}"


def key(*parts):
    """검색용 문자열. 공백을 지워 '글렌 피딕'으로도 '글렌피딕'이 잡히게 한다."""
    return re.sub(r"\s+", "", " ".join(str(p) for p in parts if p)).lower()


# ─────────────────────────────────────────────────────────────────
# 섹션 조립
# ─────────────────────────────────────────────────────────────────

def signatures():
    cards = []
    for ko, en, price, spec, abv, desc in D.SIGNATURES:
        specs = "".join(f"<li>{e(s)}</li>" for s in spec)
        cards.append(f"""
        <article class="sig" data-q="{e(key(ko, en, ' '.join(spec)))}">
          <header class="sig__head">
            <h3 class="sig__name">{e(ko)}</h3>
            <p class="sig__en">{e(en)}</p>
          </header>
          <ul class="sig__spec">{specs}</ul>
          <p class="sig__desc">{e(desc)}</p>
          <footer class="sig__foot">
            <span class="sig__abv">Alc. {e(abv)}</span>
            <span class="sig__price">{won(price)}</span>
          </footer>
        </article>""")
    return f"""
    <section class="band" id="signature" aria-labelledby="signature-h">
      <div class="band__head">
        <p class="eyebrow">Signature</p>
        <h2 class="h-band" id="signature-h">시그니처 칵테일</h2>
        <p class="band__note">바에서 직접 설계한 여섯 잔입니다.</p>
      </div>
      <figure class="shot">
        <img src="assets/hero-pour.jpg" width="900" height="1200" loading="lazy" decoding="async"
             alt="붉은 조명이 든 백바 앞 카운터에 놓인 칵테일 한 잔." />
        <figcaption><b>시그니처</b><span>바 카운터에서</span></figcaption>
      </figure>
      <div class="sigs">{''.join(cards)}</div>
    </section>"""


def cocktails():
    groups = []
    for gid, gko, items, note in D.COCKTAILS:
        rows = []
        for ko, en, price, abv, desc in items:
            abv_html = f'<span class="ab">Alc. {e(abv)}</span>' if abv else ""
            rows.append(f"""
            <div class="row" data-q="{e(key(ko, en))}">
              <p class="row__name"><span class="ko">{e(ko)}</span><span class="en">{e(en)}</span></p>
              <span class="row__price">{won(price)}</span>
              <p class="row__desc">{e(desc)} {abv_html}</p>
            </div>""")
        note_html = f'<p class="grp__note">{e(note)}</p>' if note else ""
        groups.append(f"""
        <div class="grp" data-group>
          <div class="grp__head">
            <h3>{e(gko)}</h3>
            <span class="grp__tag">{e(gid)}</span>
          </div>
          <div class="rows">{''.join(rows)}</div>
          {note_html}
        </div>""")
    return f"""
    <section class="band" id="cocktail" aria-labelledby="cocktail-h">
      <div class="band__head">
        <p class="eyebrow">Cocktail</p>
        <h2 class="h-band" id="cocktail-h">클래식 칵테일</h2>
        <p class="band__note">기주별로 묶었습니다. 메뉴에 없는 클래식도 말씀해 주세요.</p>
      </div>
      <div class="grps">{''.join(groups)}</div>
    </section>"""


def pours():
    groups = []
    for gid, gko, items in D.POURS:
        rows = []
        for ko, en, p30, p60 in items:
            en_html = f'<span class="en">{e(en)}</span>' if en else ""
            rows.append(f"""
              <tr data-q="{e(key(ko, en))}">
                <td class="nm">{e(ko)} {en_html}</td>
                <td class="num">{won(p30)}</td>
                <td class="num">{won(p60) if p60 else '—'}</td>
              </tr>""")
        note = D.POUR_NOTES.get(gid)
        note_html = f'<p class="grp__note">{e(note)}</p>' if note else ""
        groups.append(f"""
        <div class="grp" data-group>
          <div class="grp__head">
            <h3>{e(gko)}</h3>
            <span class="grp__tag">{e(gid)}</span>
          </div>
          <div class="tablewrap">
            <table class="pour">
              <thead>
                <tr><th scope="col">이름</th><th scope="col" class="num">30ml</th><th scope="col" class="num">60ml</th></tr>
              </thead>
              <tbody>{''.join(rows)}</tbody>
            </table>
          </div>
          {note_html}
        </div>""")
    return f"""
    <section class="band" id="pour" aria-labelledby="pour-h">
      <div class="band__head">
        <p class="eyebrow">By the glass</p>
        <h2 class="h-band" id="pour-h">위스키 &amp; 스피릿</h2>
        <p class="band__note">
          4만원 이상 위스키는 <strong>하프(15ml)</strong>로 드실 수 있습니다. 정가의 60% 가격입니다.<br />
          하이볼로 변경 시 10,000원이 추가됩니다.
        </p>
      </div>
      <figure class="shot">
        <img src="assets/backbar.jpg" width="1125" height="1500" loading="lazy" decoding="async"
             alt="붉게 백라이트를 넣은 선반마다 위스키 병이 줄지어 선 백바." />
        <figcaption><b>백바</b><span>여기 있는 술을 잔으로 냅니다</span></figcaption>
      </figure>
      <div class="grps grps--tight">{''.join(groups)}</div>
    </section>"""


def courses():
    cards = []
    for no, name, price, drams, desc in D.COURSES:
        lis = "".join(f"<li>{e(d)}</li>" for d in drams)
        cards.append(f"""
        <article class="course" data-q="{e(key(name, ' '.join(drams)))}">
          <span class="course__n">NO. {e(no)}</span>
          <h3 class="course__t">{e(name)}</h3>
          <ol class="course__list">{lis}</ol>
          <p class="course__d">{e(desc)}</p>
          <span class="course__price">{won(price)}</span>
        </article>""")
    return f"""
    <section class="band" id="course" aria-labelledby="course-h">
      <div class="band__head">
        <p class="eyebrow">Tasting course</p>
        <h2 class="h-band" id="course-h">테이스팅 코스</h2>
        <p class="band__note">세 잔을 각 15ml씩 나란히 냅니다. 비교하며 마시기 위한 구성입니다.</p>
      </div>
      <figure class="shot">
        <img src="assets/flight.jpg" width="1600" height="1200" loading="lazy" decoding="async"
             alt="나무 받침에 나란히 놓인 위스키 플라이트 네 잔과 곁들임 치즈 보드." />
        <figcaption><b>플라이트</b><span>나란히 놓고 비교합니다</span></figcaption>
      </figure>
      <div class="courses">{''.join(cards)}</div>
    </section>"""


def food():
    groups = []
    for gen, gko, items in D.FOOD:
        rows = []
        for ko, en, price, desc in items:
            rows.append(f"""
            <div class="row" data-q="{e(key(ko, en))}">
              <p class="row__name"><span class="ko">{e(ko)}</span><span class="en">{e(en)}</span></p>
              <span class="row__price">{won(price)}</span>
              <p class="row__desc">{e(desc)}</p>
            </div>""")
        groups.append(f"""
        <div class="grp" data-group>
          <div class="grp__head">
            <h3>{e(gen)}</h3>
            <span class="grp__tag">{e(gko)}</span>
          </div>
          <div class="rows">{''.join(rows)}</div>
        </div>""")

    beer_rows = "".join(f"""
        <div class="row" data-q="{e(key(ko, en))}">
          <p class="row__name"><span class="ko">{e(ko)}</span><span class="en">{e(en)}</span>
             <span class="spec">{e(spec)}</span></p>
          <span class="row__price">{won(price)}</span>
          <p class="row__desc">{e(desc)}</p>
        </div>""" for ko, en, price, spec, desc in D.BEERS)

    cidre_rows = "".join(f"""
        <div class="row" data-q="{e(key(ko, en))}">
          <p class="row__name"><span class="ko">{e(ko)}</span><span class="en">{e(en)}</span>
             <span class="spec">{e(spec)}</span></p>
          <span class="row__price">{won(price)}</span>
          <p class="row__desc">{e(desc)}</p>
        </div>""" for ko, en, price, spec, desc in D.CIDRES)

    return f"""
    <section class="band" id="food" aria-labelledby="food-h">
      <div class="band__head">
        <p class="eyebrow">Food</p>
        <h2 class="h-band" id="food-h">안주</h2>
        <p class="band__note">잔의 순서에 맞춰 세 묶음으로 나눴습니다.</p>
      </div>
      <div class="grps">{''.join(groups)}
        <div class="grp" data-group>
          <div class="grp__head"><h3>맥주</h3><span class="grp__tag">Beer</span></div>
          <div class="rows">{beer_rows}</div>
        </div>
        <div class="grp" data-group>
          <div class="grp__head"><h3>시드르</h3><span class="grp__tag">Cidre · 750ml</span></div>
          <p class="grp__intro">{e(D.CIDRE_INTRO)}</p>
          <div class="rows">{cidre_rows}</div>
        </div>
      </div>
    </section>"""


def bottles():
    rows = "".join(f"""
        <div class="row row--tight" data-q="{e(key(ko, en))}">
          <p class="row__name"><span class="ko">{e(ko)}</span><span class="en">{e(en)}</span></p>
          <span class="row__price">{won(price)}</span>
        </div>""" for ko, en, price in D.BOTTLES)
    return f"""
    <section class="band" id="bottle" aria-labelledby="bottle-h">
      <div class="band__head">
        <p class="eyebrow">Bottle &amp; keeping</p>
        <h2 class="h-band" id="bottle-h">보틀 · 키핑</h2>
        <p class="band__note">
          키핑 기간은 <strong>1개월</strong>, 키핑 차지는 1인 10,000원입니다.
        </p>
      </div>
      <div class="grps">
        <div class="grp" data-group>
          <div class="rows rows--two">{rows}</div>
        </div>
      </div>
    </section>"""


def info():
    return """
    <section class="band band--info" id="info" aria-labelledby="info-h">
      <div class="band__head">
        <p class="eyebrow">Information</p>
        <h2 class="h-band" id="info-h">안내</h2>
      </div>
      <div class="cards">
        <article class="card">
          <h3>쿠폰</h3>
          <p>아래 중 하나에 해당하면 도장 한 개를 적립해 드립니다.</p>
          <ul>
            <li>10만원 이상 결제</li>
            <li>테이스팅 코스 이용</li>
            <li>이 주의 위스키 2바틀 이상 주문</li>
          </ul>
          <p class="card__fine">
            중복 적립은 되지 않습니다. 조건 여러 개에 해당해도 도장은 한 개입니다.<br />
            도장 5개, 10개를 모으면 칵테일 한 잔을 드립니다.<br />
            유효기간은 마지막 도장으로부터 한 달이며, 다음 방문 시 사용하실 수 있습니다.
          </p>
        </article>
        <article class="card">
          <h3>콜키지</h3>
          <dl class="kv">
            <div><dt>와인</dt><dd>1병 100,000</dd></div>
            <div><dt>증류주</dt><dd>1병 150,000</dd></div>
          </dl>
        </article>
        <article class="card">
          <h3>주문</h3>
          <ul>
            <li>4만원 이상 위스키는 하프(15ml)로 드실 수 있습니다. 정가의 60%입니다.</li>
            <li>위스키를 하이볼로 변경하시면 10,000원이 추가됩니다.</li>
            <li>진은 원하시는 것으로 변경 가능하며 차액이 추가됩니다.</li>
            <li>진토닉으로 변경 시 3,000원이 추가됩니다.</li>
          </ul>
        </article>
      </div>
    </section>"""


# ─────────────────────────────────────────────────────────────────
# 페이지
# ─────────────────────────────────────────────────────────────────

NAV = [
    ("signature", "시그니처"),
    ("cocktail", "칵테일"),
    ("pour", "위스키"),
    ("course", "코스"),
    ("food", "안주"),
    ("bottle", "보틀"),
    ("info", "안내"),
]


def build():
    nav = "".join(f'<a href="#{i}">{e(t)}</a>' for i, t in NAV)
    body = "".join([
        signatures(), cocktails(), pours(), courses(), food(), bottles(), info(),
    ])
    total = sum(len(items) for _, _, items in D.POURS)

    return TEMPLATE.format(nav=nav, body=body, total=total, css=CSS, js=JS)


CSS = r"""
:root {
  --bg:        #E6EAE2;
  --bg-sunk:   #DAE0D6;
  --bg-raise:  #F1F4EE;
  --ink:       #0F211F;
  --ink-2:     #435855;
  --ink-3:     #798E89;
  --line:      #C2CCC3;
  --line-soft: #D4DBD2;
  --cask:      #A2650F;
  --verdigris: #2F6B65;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg:        #070F11;
    --bg-sunk:   #050B0C;
    --bg-raise:  #0D1A1C;
    --ink:       #E7EDE9;
    --ink-2:     #9FB2AE;
    --ink-3:     #677C79;
    --line:      #1C2E31;
    --line-soft: #142225;
    --cask:      #DFA352;
    --verdigris: #4F9990;
  }
}
:root[data-theme="dark"] {
  --bg:        #070F11;
  --bg-sunk:   #050B0C;
  --bg-raise:  #0D1A1C;
  --ink:       #E7EDE9;
  --ink-2:     #9FB2AE;
  --ink-3:     #677C79;
  --line:      #1C2E31;
  --line-soft: #142225;
  --cask:      #DFA352;
  --verdigris: #4F9990;
}
:root {
  --display: 'Iowan Old Style', 'Palatino Linotype', 'Hoefler Text', Palatino, Georgia,
             'Apple Myungjo', 'Nanum Myeongjo', 'Batang', serif;
  --body:    'Pretendard Variable', Pretendard, -apple-system, 'Apple SD Gothic Neo',
             'Noto Sans KR', 'Malgun Gothic', system-ui, sans-serif;
  --data:    ui-monospace, 'SF Mono', 'JetBrains Mono', 'Roboto Mono', Menlo, monospace;
  --gutter: clamp(1.1rem, 4vw, 3.5rem);
  --wide: 74rem;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--body);
  font-size: 16px;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
  word-break: keep-all;
  overflow-wrap: break-word;
}
a { color: inherit; }
:focus-visible { outline: 2px solid var(--cask); outline-offset: 3px; }

.eyebrow {
  font-family: var(--data);
  font-size: .64rem;
  letter-spacing: .22em;
  text-transform: uppercase;
  color: var(--verdigris);
  margin: 0;
}

/* ── 표지 ─────────────────────────────────── */
.cover {
  background: var(--bg-sunk);
  padding: clamp(2.5rem, 8vh, 5rem) var(--gutter) clamp(2rem, 5vh, 3rem);
  border-bottom: 1px solid var(--line);
}
.cover__in { max-width: var(--wide); margin: 0 auto; display: flex; flex-direction: column; gap: 1.1rem; }
.cover__mark {
  font-family: var(--display);
  font-weight: 400;
  font-size: clamp(2.4rem, 8.5vw, 6rem);
  line-height: .95;
  letter-spacing: .04em;
  margin: 0;
}
.cover__mark span { display: block; }
.cover__sub {
  font-family: var(--data);
  font-size: .7rem;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--ink-3);
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: .4rem 1.2rem;
}
.cover__say {
  margin: 0;
  max-width: 34rem;
  color: var(--ink-2);
  font-size: .95rem;
  padding-left: 1rem;
  border-left: 2px solid var(--cask);
}
.cover__unit {
  margin: 0;
  font-family: var(--data);
  font-size: .66rem;
  letter-spacing: .12em;
  color: var(--ink-3);
  text-transform: uppercase;
}

/* ── 도구 막대 ────────────────────────────── */
.bar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: color-mix(in oklab, var(--bg) 90%, transparent);
  backdrop-filter: blur(14px) saturate(1.3);
  border-bottom: 1px solid var(--line-soft);
}
.bar__in {
  max-width: var(--wide);
  margin: 0 auto;
  padding: .6rem var(--gutter);
  display: flex;
  align-items: center;
  gap: .8rem;
  flex-wrap: wrap;
}
.bar__nav { display: flex; gap: .15rem; flex-wrap: wrap; margin-right: auto; }
.bar__nav a {
  font-family: var(--data);
  font-size: .66rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  text-decoration: none;
  color: var(--ink-3);
  padding: .35rem .6rem;
  border: 1px solid transparent;
  transition: color .2s, border-color .2s;
}
.bar__nav a:hover { color: var(--cask); border-color: var(--line); }

.find { position: relative; display: flex; align-items: center; }
.find input {
  font-family: var(--body);
  font-size: .85rem;
  color: var(--ink);
  background: var(--bg-raise);
  border: 1px solid var(--line);
  padding: .45rem .7rem .45rem 2rem;
  width: 15rem;
  max-width: 46vw;
}
.find input::placeholder { color: var(--ink-3); }
.find svg { position: absolute; left: .6rem; color: var(--ink-3); pointer-events: none; }
.find__count {
  font-family: var(--data);
  font-size: .64rem;
  letter-spacing: .1em;
  color: var(--cask);
  margin-left: .6rem;
  white-space: nowrap;
}
.theme-toggle {
  border: 1px solid var(--line);
  background: transparent;
  color: var(--ink-2);
  width: 32px; height: 32px;
  display: grid; place-items: center;
  cursor: pointer;
  transition: border-color .2s, color .2s;
}
.theme-toggle:hover { border-color: var(--cask); color: var(--cask); }

/* ── 밴드 ─────────────────────────────────── */
.band {
  max-width: var(--wide);
  margin: 0 auto;
  padding: clamp(3rem, 8vh, 5.5rem) var(--gutter);
  border-top: 1px solid var(--line-soft);
}
.band:first-of-type { border-top: 0; }
.band__head { display: flex; flex-direction: column; gap: .5rem; margin-bottom: 2.5rem; }
.h-band {
  font-family: var(--display);
  font-weight: 400;
  font-size: clamp(1.7rem, 4vw, 2.6rem);
  line-height: 1.15;
  margin: 0;
  text-wrap: balance;
}
.band__note { margin: 0; color: var(--ink-2); font-size: .9rem; max-width: 42rem; }
.band__note strong { color: var(--ink); font-weight: 600; }

/* ── 사진 ─────────────────────────────────── */
/* 메뉴판에서 사진은 거들 뿐 — 목록을 밀어내지 않게 폭을 묶는다 */
.shot { margin: 0 0 2rem; max-width: 40rem; display: flex; flex-direction: column; gap: .55rem; }
.shot img {
  width: 100%; height: auto; display: block;
  aspect-ratio: 16 / 9; object-fit: cover;
  border: 1px solid var(--line);
  background: var(--bg-sunk);
}
.shot figcaption {
  font-family: var(--data);
  font-size: .62rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--ink-3);
  display: flex; flex-wrap: wrap; gap: .2rem .7rem;
}
.shot figcaption b { color: var(--verdigris); font-weight: 400; }

/* ── 시그니처 ─────────────────────────────── */
.sigs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
  gap: 1px;
  background: var(--line-soft);
  border: 1px solid var(--line-soft);
}
.sig {
  background: var(--bg);
  padding: 1.5rem 1.4rem;
  display: flex;
  flex-direction: column;
  gap: .9rem;
}
.sig__head { display: flex; flex-direction: column; gap: .1rem; }
.sig__name { font-family: var(--display); font-size: 1.3rem; font-weight: 400; margin: 0; }
.sig__en {
  font-family: var(--data);
  font-size: .6rem;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--ink-3);
  margin: 0;
}
.sig__spec {
  margin: 0; padding: 0; list-style: none;
  display: flex; flex-direction: column; gap: .1rem;
  font-family: var(--data);
  font-size: .7rem;
  color: var(--verdigris);
  line-height: 1.6;
}
.sig__desc { margin: 0; font-size: .88rem; color: var(--ink-2); flex: 1; }
.sig__foot {
  display: flex; align-items: baseline; justify-content: space-between;
  gap: 1rem; padding-top: .8rem; border-top: 1px solid var(--line-soft);
}
.sig__abv { font-family: var(--data); font-size: .64rem; letter-spacing: .1em; color: var(--ink-3); }
.sig__price { font-family: var(--data); font-size: 1rem; font-variant-numeric: tabular-nums; }

/* ── 그룹 · 행 ────────────────────────────── */
.grps { display: flex; flex-direction: column; gap: 3rem; }
.grps--tight { gap: 2.2rem; }
.grp { display: flex; flex-direction: column; gap: .9rem; }
.grp__head {
  display: flex; align-items: baseline; gap: .8rem;
  padding-bottom: .5rem; border-bottom: 1px solid var(--ink);
}
.grp__head h3 { font-family: var(--display); font-size: 1.3rem; font-weight: 400; margin: 0; }
.grp__tag {
  font-family: var(--data);
  font-size: .6rem;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--ink-3);
  margin-left: auto;
}
.grp__note, .grp__intro { margin: 0; font-size: .82rem; color: var(--ink-3); }
.grp__intro { max-width: 46rem; padding-bottom: .3rem; }

.rows { display: flex; flex-direction: column; }
.rows--two {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(19rem, 1fr));
  column-gap: 2.5rem;
}
.row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  column-gap: .9rem;
  row-gap: .2rem;
  padding: .9rem 0;
  border-bottom: 1px dashed var(--line-soft);
}
.row--tight { padding: .6rem 0; }
.row:hover { background: color-mix(in oklab, var(--cask) 6%, transparent); }
.row__name {
  margin: 0; font-size: .98rem; font-weight: 600;
  display: flex; align-items: baseline; gap: .5rem; flex-wrap: wrap;
}
.row__name .en, .spec {
  font-family: var(--data);
  font-size: .62rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--ink-3);
  font-weight: 400;
}
.spec { color: var(--verdigris); }
.row__price {
  font-family: var(--data); font-size: .9rem;
  font-variant-numeric: tabular-nums; white-space: nowrap; padding-top: .1rem;
}
.row__desc {
  grid-column: 1 / -1; margin: 0;
  font-size: .86rem; color: var(--ink-2); max-width: 48rem;
}
.ab {
  font-family: var(--data); font-size: .62rem;
  letter-spacing: .1em; color: var(--ink-3); white-space: nowrap;
}

/* ── 위스키 표 ────────────────────────────── */
/* 이름과 가격이 눈으로 이어지도록 폭을 묶어 둔다 */
#pour .grp { max-width: 58rem; }
.tablewrap { overflow-x: auto; }
.pour { width: 100%; min-width: 30rem; border-collapse: collapse; font-size: .92rem; }
.pour th {
  text-align: left;
  font-family: var(--data);
  font-size: .58rem;
  letter-spacing: .16em;
  text-transform: uppercase;
  color: var(--ink-3);
  font-weight: 400;
  padding: .4rem .8rem .4rem 0;
  border-bottom: 1px solid var(--line);
}
.pour th.num, .pour td.num { text-align: right; padding-right: 0; }
.pour td {
  padding: .62rem .8rem .62rem 0;
  border-bottom: 1px solid var(--line-soft);
  vertical-align: baseline;
}
.pour td.num {
  font-family: var(--data);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  color: var(--ink-2);
  width: 5.5rem;
}
.pour td.nm { color: var(--ink); font-weight: 600; }
.pour td.nm .en {
  font-family: var(--data);
  font-size: .62rem;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--ink-3);
  font-weight: 400;
  margin-left: .4rem;
}
.pour tbody tr:hover td { background: color-mix(in oklab, var(--cask) 6%, transparent); }

/* ── 코스 ─────────────────────────────────── */
.courses {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr));
  gap: 1px;
  background: var(--line-soft);
  border: 1px solid var(--line-soft);
}
.course {
  background: var(--bg);
  padding: 1.5rem 1.4rem;
  display: flex; flex-direction: column; gap: .7rem;
}
.course__n {
  font-family: var(--data); font-size: .62rem;
  letter-spacing: .2em; color: var(--cask);
}
.course__t { font-family: var(--display); font-size: 1.35rem; font-weight: 400; margin: 0; }
.course__list {
  margin: 0; padding: 0; list-style: none;
  display: flex; flex-direction: column; gap: .2rem;
  font-family: var(--data); font-size: .72rem; color: var(--verdigris);
  border-top: 1px solid var(--line-soft);
  border-bottom: 1px solid var(--line-soft);
  padding: .7rem 0;
}
.course__d { margin: 0; font-size: .86rem; color: var(--ink-2); flex: 1; }
.course__price {
  font-family: var(--data); font-size: 1rem;
  font-variant-numeric: tabular-nums;
}

/* ── 안내 ─────────────────────────────────── */
.band--info { background: var(--bg-sunk); max-width: none; }
.band--info > * { max-width: var(--wide); margin-inline: auto; }
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
  gap: 1.5rem;
}
.card {
  border: 1px solid var(--line);
  padding: 1.4rem;
  display: flex; flex-direction: column; gap: .7rem;
  background: var(--bg);
}
.card h3 { font-family: var(--display); font-size: 1.15rem; font-weight: 400; margin: 0; }
.card p { margin: 0; font-size: .88rem; color: var(--ink-2); }
.card ul { margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: .4rem; }
.card li {
  position: relative; padding-left: 1rem;
  font-size: .88rem; color: var(--ink-2);
}
.card li::before {
  content: ""; position: absolute; left: 0; top: .68em;
  width: 5px; height: 5px; background: var(--verdigris);
}
.card__fine { font-size: .8rem !important; color: var(--ink-3) !important; }
.kv { margin: 0; display: flex; flex-direction: column; gap: .4rem; }
.kv div { display: flex; justify-content: space-between; gap: 1rem; border-bottom: 1px dotted var(--line); padding: .3rem 0; }
.kv dt { font-size: .88rem; color: var(--ink-2); }
.kv dd { margin: 0; font-family: var(--data); font-variant-numeric: tabular-nums; font-size: .88rem; }

/* ── 검색 상태 ────────────────────────────── */
[hidden] { display: none !important; }
.empty {
  display: none;
  padding: 3rem var(--gutter);
  text-align: center;
  color: var(--ink-3);
  font-size: .95rem;
  max-width: var(--wide);
  margin: 0 auto;
}
body[data-empty="true"] .empty { display: block; }

/* ── 꼬리말 ───────────────────────────────── */
.foot {
  border-top: 1px solid var(--line);
  padding: 2.5rem var(--gutter) 4rem;
  background: var(--bg-sunk);
}
.foot__in {
  max-width: var(--wide); margin: 0 auto;
  display: flex; flex-wrap: wrap; gap: 1.2rem; align-items: flex-end;
}
.foot__mark {
  font-family: var(--display);
  font-size: clamp(1.6rem, 5vw, 2.8rem);
  line-height: 1; margin: 0 auto 0 0; letter-spacing: .06em;
}
.foot__meta {
  font-family: var(--data); font-size: .64rem;
  letter-spacing: .12em; text-transform: uppercase;
  color: var(--ink-3); text-align: right;
  display: flex; flex-direction: column; gap: .3rem;
}
.foot__meta a { text-decoration: none; }
.foot__meta a:hover { color: var(--cask); }

/* ── 인쇄 ─────────────────────────────────── */
@media print {
  .bar, .theme-toggle, .shot { display: none !important; }
  body { background: #fff; color: #000; font-size: 10.5pt; }
  .cover, .band--info, .foot { background: #fff; }
  .band { padding: .8rem 0; max-width: none; }
  .grp, .sig, .course, .card, .row { break-inside: avoid; }
  .band { break-before: page; }
  .band:first-of-type { break-before: auto; }
  .sigs, .courses { border: 0; background: none; gap: 0; }
  .sig, .course { padding: .5rem 0; }
}
"""

JS = r"""
(function () {
  var root = document.documentElement;
  var btn = document.getElementById('themeBtn');
  btn.addEventListener('click', function () {
    var dark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    var now = root.getAttribute('data-theme') || (dark ? 'dark' : 'light');
    root.setAttribute('data-theme', now === 'dark' ? 'light' : 'dark');
  });

  /* ── 찾기 ────────────────────────────────
     data-q 에 한글·영문을 공백 없이 담아 두었다.
     검색어도 같은 방식으로 눌러 비교하므로
     '글렌 피딕' 으로도 '글렌피딕' 이 걸린다.        */
  var input = document.getElementById('find');
  var count = document.getElementById('findCount');
  var items = Array.prototype.slice.call(document.querySelectorAll('[data-q]'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('[data-group]'));
  var bands = Array.prototype.slice.call(document.querySelectorAll('.band'));

  function squash(s) { return s.replace(/\s+/g, '').toLowerCase(); }

  function run() {
    var q = squash(input.value);
    if (!q) {
      items.forEach(function (n) { n.hidden = false; });
      groups.concat(bands).forEach(function (n) { n.hidden = false; });
      count.textContent = '';
      document.body.setAttribute('data-empty', 'false');
      return;
    }
    var hits = 0;
    items.forEach(function (n) {
      var on = n.getAttribute('data-q').indexOf(q) !== -1;
      n.hidden = !on;
      if (on) hits++;
    });
    /* 안에 남은 항목이 없는 그룹과 섹션은 통째로 접는다 */
    groups.forEach(function (g) {
      g.hidden = !g.querySelector('[data-q]:not([hidden])');
    });
    bands.forEach(function (b) {
      if (b.id === 'info') { b.hidden = true; return; }
      b.hidden = !b.querySelector('[data-q]:not([hidden])');
    });
    count.textContent = hits + '건';
    document.body.setAttribute('data-empty', hits === 0 ? 'true' : 'false');
  }

  input.addEventListener('input', run);
  input.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') { input.value = ''; run(); }
  });
})();
"""

TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Uisce Beatha — 메뉴판</title>
<meta name="description" content="위스키 {total}종, 시그니처와 클래식 칵테일, 테이스팅 코스와 안주. Uisce Beatha 메뉴." />
<style>{css}</style>
</head>
<body data-empty="false">

<header class="cover">
  <div class="cover__in">
    <p class="eyebrow">Since 2023</p>
    <h1 class="cover__mark"><span>Uisce</span><span>Beatha</span></h1>
    <p class="cover__sub">
      <span>Whiskey &amp; Classic Cocktail</span>
      <span>위스키 {total}종</span>
      <span>@uiscebeatha_bar</span>
    </p>
    <p class="cover__say">
      첫 잔이 가장 중요합니다. 바텐더에게 묻는 걸 어려워하지 않으셔도 됩니다.
      주문과 요청 시 손만 살짝 들어주세요.
    </p>
    <p class="cover__unit">가격 단위 : 원 (부가세 포함)</p>
  </div>
</header>

<div class="bar">
  <div class="bar__in">
    <nav class="bar__nav" aria-label="메뉴 분류">{nav}</nav>
    <div class="find">
      <svg width="13" height="13" viewBox="0 0 16 16" aria-hidden="true" focusable="false">
        <circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.4" />
        <path d="M11 11l4 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" />
      </svg>
      <label class="sr-only" for="find" hidden>메뉴 찾기</label>
      <input id="find" type="search" placeholder="술 이름으로 찾기" autocomplete="off" />
    </div>
    <span class="find__count" id="findCount" role="status" aria-live="polite"></span>
    <button class="theme-toggle" type="button" id="themeBtn" aria-label="밝기 전환">
      <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true" focusable="false">
        <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.2" />
        <path d="M8 2a6 6 0 0 0 0 12z" fill="currentColor" />
      </svg>
    </button>
  </div>
</div>

<main>
{body}
  <p class="empty">찾으시는 술이 목록에 없습니다. 바텐더에게 물어봐 주세요.</p>
</main>

<footer class="foot">
  <div class="foot__in">
    <p class="foot__mark">Uisce Beatha</p>
    <div class="foot__meta">
      <a href="https://instagram.com/uiscebeatha_bar" rel="noreferrer">@uiscebeatha_bar</a>
      <span>Whiskey &amp; Classic Cocktail · Since 2023</span>
    </div>
  </div>
</footer>

<script>{js}</script>
</body>
</html>
"""


if __name__ == "__main__":
    OUT.write_text(build(), encoding="utf-8")
    n = sum(len(i) for _, _, i in D.POURS)
    print(f"menu.html 생성 완료 — 위스키·스피릿 {n}종, {OUT.stat().st_size:,} bytes")
