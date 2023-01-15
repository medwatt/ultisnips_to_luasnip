# Sample

See [test.snippets](./test.snippets) for the original snippets.

This tool depends on [lark](https://github.com/lark-parser/lark) for parsing. It can be installed with `pip install lark`.

```lua
s(
        {trig="bye", dscr="My mail signature"},
        {
                t({ 'Good bye, Sir. Hope to talk to you soon.', '- Arthur, King of Britain' })
        }
),

s(
        {trig="match", dscr="Structural pattern matching"},
        {
                t('match '),
                i(1, 'expression'),
                t({ ':', '    case ' }),
                i(2, 'pattern_1'),
                t({ ':', '        ' }),
                i(3, 'pass'),
                t({ '', '    case ' }),
                i(4, 'pattern_2'),
                t({ ':', '        ' }),
                i(0, 'pass')
        }
),

s(
        {trig="cc", dscr="Capacitor", snippetType="autosnippet"},
        {
                t('C'),
                i(1),
                t(' '),
                i(2, 'N+'),
                t(' '),
                i(3, 'N-'),
                t(' '),
                i(4, 'value'),
                c(5, { sn(nil, { t(' '), i(1, 'a_1'), t(' '), i(2, 'a_2') } ), t('') } )
        }
),

s(
        {trig="q"},
        {
                t('Your age: '),
                c(1, { t('<18'), t('18~60'), t('>60') }),
                t({ '', 'Your height: ' }),
                c(2, { t('<120cm'), t('120cm~180cm'), t('>180cm') })
        }
),

s(
        {trig="dint", dscr="definit integral", snippetType="autosnippet"},
        {
                t('\\int_{'),
                i(1, '-\\infty'),
                t('}^{'),
                i(2, '\\infty'),
                t('} '),
                i(3, 'integrand'),
                t(' {\\mathrm{d} '),
                i(4, 'x'),
                t('}')
        },

        { condition = math }
),
```
