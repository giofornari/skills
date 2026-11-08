import { Bar, Caret, Card, Prompt, Row, Stage, Text, Window } from '../../kit'
import './hero.css'

// README hero (960 × 400, dark): a terminal installing a pack, and the pack list
// (the /plugin panel's first rows) straddling its right edge. Real words only on
// the commands, the result and the first three packs; the rest of the list is filler
// that the bottom crop takes.
const PACKS: { id: string; color: string; tokens: string; selected?: boolean }[] = [
  { id: '1-pack-fundamentals', color: '#929292', tokens: '~3,704', selected: true },
  { id: '2-pack-context-memory', color: '#761717', tokens: '~3,710' },
  { id: '3-pack-design', color: '#ff8c38', tokens: '~4,417' },
]
const FILLER = [
  { color: '#3cbc36', name: 92 },
  { color: '#fb7081', name: 70 },
  { color: '#1c70a5', name: 84 },
]

export default function HeroInstall() {
  return (
    <div className="hi">
      <Stage width={960} height={400} theme="dark" className="hi-stage">
        {() => (
          <>
            <Window chrome="terminal" lights="grey" title="claude — ~/app" className="hi-term">
              <div className="ss-term hi-term__body">
                <Prompt path="~/app">/plugin marketplace add giofornari/skills</Prompt>
                <div><span className="ok">✓</span> <span className="dim">Added</span> giofornari</div>
                <Prompt path="~/app">/plugin marketplace add thedotmack/claude-mem</Prompt>
                <div><span className="ok">✓</span> <span className="dim">Added</span> claude-mem</div>
                <Prompt path="~/app">/plugin install 1-pack-fundamentals@giofornari</Prompt>
                <div><span className="ok">✓</span> <span className="dim">Installed</span> 8 plugins</div>
                <Prompt path="~/app">/reload-plugins</Prompt>
                <div><span className="ok">✓</span> <span className="dim">Reloaded</span> 8 plugins</div>
                <Prompt path="~/app">
                  <Caret />
                </Prompt>
              </div>
            </Window>
            <Card pad="medium" lift className="hi-packs" data-target="packs">
              <Text className="hi-packs__title">Packs</Text>
              <div className="hi-list">
                {PACKS.map(p => (
                  <Row
                    key={p.id}
                    pad={0}
                    selected={p.selected}
                    className="hi-row"
                    lead={<span className="hi-swatch" style={{ background: p.color }} />}
                    title={<Text className="hi-name">{p.id}</Text>}
                  >
                    <Text className="hi-tokens">{p.tokens}</Text>
                  </Row>
                ))}
                {FILLER.map((p, i) => (
                  <Row key={i} pad={0} className="hi-row" lead={<span className="hi-swatch" style={{ background: p.color }} />} title={<Bar w={p.name} tone={3} />}>
                    <Bar w={34} tone={2} />
                  </Row>
                ))}
              </div>
            </Card>
          </>
        )}
      </Stage>
    </div>
  )
}
