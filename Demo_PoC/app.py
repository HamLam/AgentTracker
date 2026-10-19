"""AgentTracker browser prototype. All activities are explicitly simulated."""
import argparse
from datetime import datetime
from nicegui import ui

AREAS = ['Project workspace', 'Execution & processes', 'System & environment', 'External services']
SCENES = [
    ('Reading project files', 'cat README.md', '/project/README.md', [0, 1]),
    ('Running tests', 'python -m pytest', '/project/tests', [0, 1]),
    ('Inspecting environment', 'python -m pip list', '/project/.venv', [1, 2]),
    ('Pushing changes', 'git push origin main', 'github.com/HamLam/AgentTracker', [1, 3]),
    ('Idle · waiting for a task', 'No command running', '/project', []),
]

CSS = '''
body {background:#090f1c;color:#dce6f6;font-family:ui-sans-serif,system-ui,sans-serif}
.nicegui-content {max-width:1440px;margin:auto;padding:30px;width:100%}
.panel {background:#101b2c;border:1px solid #253349;border-radius:18px;padding:24px}
.muted {color:#93a6bf} .eyebrow {color:#72d9d1;letter-spacing:3px;font-size:11px;font-weight:700}
.layout {display:grid;grid-template-columns:minmax(0,1.5fr) minmax(300px,1fr);gap:22px;width:100%}
.radar svg {width:100%;max-height:560px;display:block} .radar {width:100%}
.q-btn {text-transform:none;border-radius:9px} .details {overflow-wrap:anywhere}
.sector {cursor:pointer;transition:fill .3s} .sector:hover {filter:brightness(1.5)}
@media(max-width:850px){.layout{grid-template-columns:1fr}.nicegui-content{padding:16px}}
'''


def radar_svg(active, selected, connected=True):
    paths = ['M300 300 L60 300 A240 240 0 0 1 300 60 Z',
             'M300 300 L300 60 A240 240 0 0 1 540 300 Z',
             'M300 300 L300 540 A240 240 0 0 1 60 300 Z',
             'M300 300 L540 300 A240 240 0 0 1 300 540 Z']
    coords = [(190,190),(410,190),(190,410),(410,410)]
    labels = [('PROJECT','WORKSPACE'),('EXECUTION','& PROCESSES'),('SYSTEM','& ENVIRONMENT'),('EXTERNAL','SERVICES')]
    parts = ['<svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Four quadrant agent activity radar">']
    for i, path in enumerate(paths):
        color = '#64748b' if not connected else '#fb7185' if i in active else '#34d399'
        status = 'UNKNOWN' if not connected else '1 AGENT ACTIVE' if i in active else 'NO ACTIVE AGENT'
        x,y = coords[i]
        parts.append(f'<g data-q="{i}" class="sector"><path d="{path}" fill="{color}" fill-opacity=".14" stroke="{color}" stroke-width="{3 if i == selected else 1}"/><text x="{x}" y="{y-15}" text-anchor="middle" fill="#e2e8f0" font-size="14" font-weight="700">{labels[i][0]}</text><text x="{x}" y="{y+5}" text-anchor="middle" fill="#e2e8f0" font-size="12">{labels[i][1]}</text><text x="{x}" y="{y+32}" text-anchor="middle" fill="{color}" font-size="10">{status}</text></g>')
    for r in (80,160,240):
        parts.append(f'<circle cx="300" cy="300" r="{r}" fill="none" stroke="#8aa4c0" stroke-opacity=".16" pointer-events="none"/>')
    parts.append('<circle cx="300" cy="300" r="30" fill="#101b2c" stroke="#6386a6" pointer-events="none"/><text x="300" y="305" text-anchor="middle" fill="#a5f3fc" font-size="12" pointer-events="none">AT</text></svg>')
    return ''.join(parts)


@ui.page('/')
def dashboard():
    ui.add_css(CSS)
    state = {'last_target':SCENES[0][2], 'scene':0, 'selected':0, 'auto':True, 'connected':True,
             'updated':datetime.now().strftime('%H:%M:%S'), 'history':[]}
    ui.label('AGENTTRACKER / OBSERVATORY').classes('eyebrow')
    with ui.row().classes('w-full items-center justify-between'):
        ui.label('Agent Activity Tracker').classes('text-3xl font-bold')
        ui.badge('SIMULATED DATA · DEMO').props('outline color=amber')
    ui.label('Explore four operating areas. Select a quadrant to inspect its activity.').classes('muted mb-4')
    with ui.row().classes('w-full items-center gap-3 mb-3'):
        ui.switch('Auto-play demo', value=True, on_change=lambda e: state.update(auto=e.value))
        ui.button('Next activity', on_click=lambda: advance()).props('outline')
        ui.button('Set idle', on_click=lambda: set_scene(4)).props('outline')
        ui.switch('Feed connected', value=True, on_change=lambda e: connection(e.value))
    with ui.element('div').classes('layout'):
        with ui.column().classes('panel w-full'):
            with ui.row().classes('w-full justify-between items-center'):
                ui.label('Activity radar').classes('text-xl font-semibold')
                ui.label('01 / DEMO AGENT').classes('eyebrow')
            radar = ui.html('', sanitize=False).classes('radar')
            radar.on('click', lambda e: select(int(e.args)), js_handler='(e) => {const q=e.target.closest("[data-q]"); if(q) emit(q.dataset.q)}')
            with ui.row().classes('gap-4 text-xs'):
                ui.label('● Red · active').style('color:#fb7185')
                ui.label('● Green · no active agent').style('color:#34d399')
                ui.label('● Gray · unknown').style('color:#94a3b8')
            with ui.row().classes('gap-2'):
                for i, name in enumerate(AREAS):
                    ui.button(name, on_click=lambda i=i: select(i)).props('flat dense size=sm')
        with ui.column().classes('gap-5 w-full'):
            with ui.column().classes('panel w-full details'):
                ui.label('SELECTED AREA').classes('eyebrow')
                area = ui.label().classes('text-2xl font-semibold')
                area_status = ui.label().classes('muted')
                ui.separator().style('background:#253349')
                ui.label('DEMO AGENT / CURRENT ACTIVITY').classes('eyebrow')
                action = ui.label().classes('text-lg')
                command = ui.label().classes('font-mono text-sm').style('color:#a5f3fc')
                ui.label('TARGET / LAST KNOWN LOCATION').classes('eyebrow mt-3')
                location = ui.label().classes('font-mono text-sm muted')
                updated = ui.label().classes('text-xs muted mt-3')
            with ui.column().classes('panel w-full'):
                ui.label('Activity timeline').classes('text-xl font-semibold')
                history = ui.column().classes('w-full gap-3')
    ui.label('Prototype · No live agent monitoring is connected. Commands shown here are examples and are never executed.').classes('muted text-xs mt-5')

    def render():
        title, cmd, target, active = SCENES[state['scene']]
        radar.set_content(radar_svg(active, state['selected'], state['connected']))
        area.set_text(AREAS[state['selected']])
        area_status.set_text('Unknown · feed disconnected' if not state['connected'] else
                             '1 demo agent active here' if state['selected'] in active else 'No active agent in this area')
        action.set_text(title if state['connected'] else 'Feed disconnected · last observed activity below')
        command.set_text(cmd)
        location.set_text(state['last_target'])
        updated.set_text(f"Last demo event {state['updated']} · {'connected' if state['connected'] else 'STALE'}")
        history.clear()
        with history:
            for stamp, text in state['history'][:5]:
                with ui.row().classes('w-full gap-3 items-start'):
                    ui.label(stamp).classes('font-mono text-xs muted')
                    ui.label(text).classes('text-sm')

    def select(index):
        state['selected'] = index
        render()

    def set_scene(index):
        if not state['connected']:
            ui.notify('Reconnect the demo feed first')
            return
        state['scene'] = index
        if SCENES[index][3]:
            state['last_target'] = SCENES[index][2]
        state['updated'] = datetime.now().strftime('%H:%M:%S')
        state['history'].insert(0, (state['updated'], SCENES[index][0]))
        state['history'] = state['history'][:20]
        render()

    def advance():
        set_scene((state['scene'] + 1) % len(SCENES))

    def connection(value):
        state['connected'] = value
        if value:
            set_scene(state['scene'])
        else:
            render()

    set_scene(0)
    ui.timer(5, lambda: advance() if state['auto'] and state['connected'] else None)


if __name__ in {'__main__', '__mp_main__'}:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    ui.run(host=args.host, port=args.port, title='AgentTracker', reload=False, show=False)
