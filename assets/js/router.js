const allowed=['home','explorer','compare','detail','religions','sources','favorites'];
export function route(){const r=location.hash.slice(1).split('?')[0];return allowed.includes(r)?r:'home'}
export function startRouter(render){addEventListener('hashchange',()=>render(route()));render(route())}
