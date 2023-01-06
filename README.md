# Sample

**Text only snippet**

Input

```
snippet bye "My mail signature"
Good bye, Sir. Hope to talk to you soon.
- Arthur, King of Britain
endsnippet
```

Output

```
s(
    {
        trig = "bye",
        dscr = "My mail signature",
        regTrig = false
    },
    { t({ "Good bye, Sir. Hope to talk to you soon.", "- Arthur, King of Britain" }) }
),
```

**Snippet with tab stops**

Input

```
snippet match "Structural pattern matching" b
match ${1:expression}:
    case ${2:pattern_1}:
        ${3:pass}
    case ${4:pattern_2}:
        ${0:pass}
endsnippet
```

Output

```
    s(
        {
            trig = "match",
            dscr = "Structural pattern matching"
        },
        fmta(
            [[
match <>:
    case <>:
        <>
    case <>:
        <>
]]           ,
            {
                i(1, "expression"),
                i(2, "pattern_1"),
                i(3, "pass"),
                i(4, "pattern_2"),
                i(0, "pass")
            }
        )
    ),
```

**Snippet with VISUAL**

Input

```
snippet for "for loop" b
for ${1:item} in ${2:iterable}:
    ${3:${VISUAL:pass}}
endsnippet
```

Output

```
s(
    {
        trig = "for",
        dscr = "for loop"
    },
    fmta(
        [[
for <> in <>:
<>
]]           ,
        {
            i(1, "item"),
            i(2, "iterable"),
            d(3, get_visual("pass"))
        }
    )
),
```

**Snippet with VISUAL**

Input

```
snippet q
Your age: ${1|<18,18~60,>60|}
Your height: ${2|<120cm,120cm~180cm,>180cm|}$0$
endsnippet
```

Output

```
s(
    {
        trig = "q",
        regTrig = false
    },
    fmta(
        [[
Your age: $<>
Your height: $<>
]]           ,
        {
            c(1, { t("18"), t("18~60"), t(">60") }),
            c(2, { t("120cm"), t("120cm~180cm"), t(">180cm") }),
            i(0)
        }
    )
),
```

**Snippet with coxtext and options**

Input

```
priority 300
context "math()"
snippet dint "definit integral" wA
\int_{${1:-\infty}}^{${2:\infty}} ${3:${VISUAL}} {\mathrm{d} ${4:x}}$0
endsnippet
```

Output

```
s(
    {
        trig = "dint",
        dscr = "definit integral",
        priority = 300,
        snippetType = "autosnippet"
    },
    fmta(
        [[
\int_{<>}^{<>} <> {\mathrm{d} <>}<>
]]           ,
        {
            i(1, "-\infty"),
            i(2, "\infty"),
            d(3, get_visual),
            i(4, "x"),
            i(0)
        }
    ),
    { condition = math },
),
```
