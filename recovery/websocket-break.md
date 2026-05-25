# Recovery Playbook: WebSocket Break

## Diagnosis Tree

```
WebSocket not connecting?
  │
  ├── Browser shows "WebSocket connection failed"
  │     ├── Vite proxy not configured for WS
  │     │     → Check vite.config.ts has: '/ws/expert': { ws: true, ... }
  │     │     → Restart Vite dev server (config changes require restart)
  │     │
  │     ├── JWT token expired or missing
  │     │     → WS closes with code 4001
  │     │     → Auth store must refresh token before connecting
  │     │     → Check useExpertWS.ts: token dependency in useEffect
  │     │
  │     └── Backend not running on expected port
  │           → curl http://localhost:8002/health
  │           → Check /tmp/expert-backend.log
  │
  ├── WebSocket connects but receives no data
  │     ├── Redis Pub/Sub not running
  │     │     → redis-cli ping → should return PONG
  │     │     → If not: sudo systemctl start redis
  │     │
  │     ├── Wrong channel subscription
  │     │     → Check: ConnectionManager.subscribe() called with correct channel name
  │     │     → Channel format: "positions.<account_id>", "signals.<provider_id>"
  │     │
  │     └── Publisher not publishing to Redis
  │           → Add temporary: await redis.publish("test", "hello")
  │           → Monitor: redis-cli SUBSCRIBE test (in separate terminal)
  │
  └── WebSocket connects then immediately disconnects
        ├── CORS issue (browser rejects WS handshake)
        │     → WS connections are not subject to CORS in the same way
        │     → Check: browser console for specific error message
        │
        └── Unhandled exception in connection handler
              → Check /tmp/expert-backend.log for traceback
              → Wrap connection handler in try/except
```

---

## Debugging Commands

```bash
# Test WebSocket connection directly (wscat or websocat)
# Install: npm i -g wscat
TOKEN="<your-jwt-token>"
wscat -c "ws://localhost:8002/ws/expert?token=$TOKEN"

# Monitor all Redis pub/sub activity
redis-cli MONITOR | grep PUBLISH

# Check WebSocket frames in browser:
# DevTools → Network → WS → click connection → Messages tab

# Check backend receives connection:
tail -f /tmp/expert-backend.log | grep -E "websocket|ws|connect"
```

---

## Frontend Reconnection Verification

```typescript
// Verify WebSocket manager has proper reconnection logic
// Check WebSocketManager.ts:
//   - onclose handler calls _scheduleReconnect()
//   - exponential backoff: delay doubles on each failure (max 30s)
//   - reconnectDelay resets to 1000 on successful connection

// Add temporary debugging:
this.ws.onopen = () => {
  console.log('[WS] Connected');
  this.reconnectDelay = 1000;
};
this.ws.onclose = (event) => {
  console.log('[WS] Disconnected', event.code, event.reason);
  this._scheduleReconnect(token);
};
```

---

## Common Fix: Vite Proxy for WebSocket

```typescript
// vite.config.ts — WebSocket proxies need ws: true
export default defineConfig({
  server: {
    proxy: {
      '/ws/expert': {
        target: 'ws://localhost:8002',
        ws: true,                    // ← REQUIRED for WebSocket
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
        changeOrigin: true,
      },
    },
  },
});
// NOTE: Must restart Vite after changing proxy config
```
