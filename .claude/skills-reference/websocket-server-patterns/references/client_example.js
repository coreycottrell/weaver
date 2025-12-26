/**
 * Trading Arena WebSocket Client
 *
 * JavaScript/TypeScript client for connecting to the Trading Arena
 * WebSocket server. Handles authentication, reconnection, heartbeats,
 * and event replay.
 *
 * Usage:
 *   const client = new TradingWebSocketClient('weaver', privateKey);
 *   await client.connect('portfolio');
 *   client.on('position_updated', (data) => console.log(data));
 *
 * Author: AI-CIV capability-curator
 * Version: 1.0.0
 * Date: 2025-12-26
 */

// For Node.js, uncomment:
// const WebSocket = require('ws');
// const { sign } = require('tweetnacl');
// const { decodeUTF8 } = require('tweetnacl-util');

/**
 * WebSocket client for Trading Arena.
 *
 * Features:
 * - Ed25519 challenge-response authentication
 * - Automatic reconnection with exponential backoff
 * - Heartbeat handling (ping/pong)
 * - Event replay on reconnection
 * - Event emitter pattern for handling updates
 */
class TradingWebSocketClient {
    /**
     * Create a new Trading WebSocket client.
     *
     * @param {string} collectiveId - Your collective's ID
     * @param {Uint8Array} privateKey - Ed25519 private key for signing
     * @param {Object} options - Configuration options
     */
    constructor(collectiveId, privateKey, options = {}) {
        this.collectiveId = collectiveId;
        this.privateKey = privateKey;

        // Configuration
        this.baseUrl = options.baseUrl || 'ws://localhost:8000/ws';
        this.maxReconnectAttempts = options.maxReconnectAttempts || 10;
        this.reconnectDelayMs = options.reconnectDelayMs || 1000;
        this.maxReconnectDelayMs = options.maxReconnectDelayMs || 30000;

        // State
        this.ws = null;
        this.stream = null;
        this.authenticated = false;
        this.reconnectAttempts = 0;
        this.lastSequence = 0;

        // Event handlers
        this._handlers = {};

        // Bind methods
        this._onOpen = this._onOpen.bind(this);
        this._onMessage = this._onMessage.bind(this);
        this._onClose = this._onClose.bind(this);
        this._onError = this._onError.bind(this);
    }

    /**
     * Connect to a WebSocket stream.
     *
     * @param {string} stream - Stream type: 'portfolio' or 'orders'
     * @returns {Promise<void>}
     */
    async connect(stream) {
        this.stream = stream;
        this.authenticated = false;

        const url = `${this.baseUrl}/${this.collectiveId}/${stream}?last_sequence=${this.lastSequence}`;

        return new Promise((resolve, reject) => {
            this._connectResolve = resolve;
            this._connectReject = reject;

            this.ws = new WebSocket(url);
            this.ws.onopen = this._onOpen;
            this.ws.onmessage = this._onMessage;
            this.ws.onclose = this._onClose;
            this.ws.onerror = this._onError;
        });
    }

    /**
     * Disconnect from the WebSocket.
     */
    disconnect() {
        this.reconnectAttempts = this.maxReconnectAttempts; // Prevent reconnection
        if (this.ws) {
            this.ws.close(1000, 'Client disconnect');
            this.ws = null;
        }
    }

    /**
     * Register an event handler.
     *
     * @param {string} eventType - Event type to listen for
     * @param {Function} handler - Handler function(data)
     */
    on(eventType, handler) {
        if (!this._handlers[eventType]) {
            this._handlers[eventType] = [];
        }
        this._handlers[eventType].push(handler);
    }

    /**
     * Remove an event handler.
     *
     * @param {string} eventType - Event type
     * @param {Function} handler - Handler to remove
     */
    off(eventType, handler) {
        if (this._handlers[eventType]) {
            this._handlers[eventType] = this._handlers[eventType].filter(h => h !== handler);
        }
    }

    /**
     * Subscribe to a specific order's updates.
     *
     * @param {string} orderId - Order ID to subscribe to
     */
    subscribeOrder(orderId) {
        this._send({
            type: 'subscribe_order',
            order_id: orderId
        });
    }

    // ==================== Internal Methods ====================

    _emit(eventType, data) {
        const handlers = this._handlers[eventType] || [];
        handlers.forEach(handler => {
            try {
                handler(data);
            } catch (e) {
                console.error(`Handler error for ${eventType}:`, e);
            }
        });

        // Also emit to wildcard handlers
        const wildcardHandlers = this._handlers['*'] || [];
        wildcardHandlers.forEach(handler => {
            try {
                handler(eventType, data);
            } catch (e) {
                console.error('Wildcard handler error:', e);
            }
        });
    }

    _send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }

    _onOpen() {
        console.log(`WebSocket connected to ${this.stream}`);
        this.reconnectAttempts = 0;
    }

    async _onMessage(event) {
        let data;
        try {
            data = JSON.parse(event.data);
        } catch (e) {
            console.error('Failed to parse WebSocket message:', e);
            return;
        }

        const type = data.type;

        // Track sequence for reconnection replay
        if (data.sequence) {
            this.lastSequence = Math.max(this.lastSequence, data.sequence);
        }

        switch (type) {
            case 'auth_challenge':
                await this._handleAuthChallenge(data);
                break;

            case 'auth_success':
                this.authenticated = true;
                console.log('Authenticated successfully');
                this._emit('authenticated', data);
                if (this._connectResolve) {
                    this._connectResolve();
                    this._connectResolve = null;
                }
                break;

            case 'auth_failure':
                console.error('Authentication failed:', data.reason);
                this._emit('auth_error', data);
                if (this._connectReject) {
                    this._connectReject(new Error(data.reason));
                    this._connectReject = null;
                }
                break;

            case 'ping':
                // Respond to server ping
                this._send({ type: 'pong' });
                break;

            case 'replay_complete':
                console.log(`Replayed ${data.replayed_count} missed events`);
                this._emit('replay_complete', data);
                break;

            case 'error':
                console.error('Server error:', data);
                this._emit('error', data);
                break;

            default:
                // All other events (portfolio_snapshot, position_updated, etc.)
                this._emit(type, data.data || data);
        }
    }

    async _handleAuthChallenge(data) {
        console.log('Received auth challenge');

        try {
            // Sign the challenge with Ed25519
            const signature = this._signChallenge(data.challenge);

            this._send({
                type: 'auth_response',
                signature: signature
            });
        } catch (e) {
            console.error('Failed to sign challenge:', e);
            this._emit('auth_error', { reason: 'Signing failed' });
        }
    }

    _signChallenge(challenge) {
        // Using tweetnacl for Ed25519 signing
        // In browser, you might use SubtleCrypto or a library

        // For tweetnacl:
        // const messageBytes = decodeUTF8(challenge);
        // const signature = sign.detached(messageBytes, this.privateKey);
        // return btoa(String.fromCharCode(...signature));

        // Placeholder - implement with your crypto library
        throw new Error('Implement _signChallenge with your Ed25519 library');
    }

    _onClose(event) {
        console.log(`WebSocket closed: ${event.code} ${event.reason}`);
        this.authenticated = false;

        // Emit close event
        this._emit('disconnected', {
            code: event.code,
            reason: event.reason
        });

        // Attempt reconnection for unexpected closes
        if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
            this._attemptReconnect();
        }
    }

    _onError(error) {
        console.error('WebSocket error:', error);
        this._emit('error', error);
    }

    _attemptReconnect() {
        this.reconnectAttempts++;

        // Exponential backoff with jitter
        const delay = Math.min(
            this.reconnectDelayMs * Math.pow(2, this.reconnectAttempts - 1),
            this.maxReconnectDelayMs
        );
        const jitter = delay * 0.2 * Math.random();
        const actualDelay = delay + jitter;

        console.log(`Reconnecting in ${Math.round(actualDelay)}ms (attempt ${this.reconnectAttempts})`);

        setTimeout(() => {
            if (this.stream) {
                this.connect(this.stream).catch(e => {
                    console.error('Reconnection failed:', e);
                });
            }
        }, actualDelay);
    }
}

// ==================== Usage Examples ====================

/**
 * Example: Portfolio streaming
 */
async function portfolioExample() {
    // In production, load private key securely
    const privateKey = new Uint8Array(64); // Your Ed25519 private key

    const client = new TradingWebSocketClient('weaver', privateKey, {
        baseUrl: 'ws://localhost:8000/ws'
    });

    // Register event handlers
    client.on('portfolio_snapshot', (data) => {
        console.log('Portfolio snapshot:', data);
    });

    client.on('position_updated', (data) => {
        console.log('Position updated:', data);
    });

    client.on('balance_updated', (data) => {
        console.log('Balance updated:', data);
    });

    client.on('disconnected', ({ code, reason }) => {
        console.log(`Disconnected: ${code} - ${reason}`);
    });

    // Connect
    try {
        await client.connect('portfolio');
        console.log('Connected to portfolio stream');
    } catch (e) {
        console.error('Failed to connect:', e);
    }
}

/**
 * Example: Orders streaming with specific order subscription
 */
async function ordersExample() {
    const privateKey = new Uint8Array(64);

    const client = new TradingWebSocketClient('weaver', privateKey);

    client.on('orders_snapshot', (orders) => {
        console.log('Active orders:', orders);
    });

    client.on('order_created', (order) => {
        console.log('New order:', order);
        // Subscribe to this specific order's updates
        client.subscribeOrder(order.order_id);
    });

    client.on('order_filled', (data) => {
        console.log('Order filled:', data);
    });

    client.on('order_cancelled', (data) => {
        console.log('Order cancelled:', data);
    });

    await client.connect('orders');
}

/**
 * Example: React hook for WebSocket
 */
function useTradingWebSocket(collectiveId, stream, privateKey) {
    // This is pseudocode for a React hook
    /*
    const [connected, setConnected] = useState(false);
    const [data, setData] = useState(null);
    const clientRef = useRef(null);

    useEffect(() => {
        const client = new TradingWebSocketClient(collectiveId, privateKey);
        clientRef.current = client;

        client.on('authenticated', () => setConnected(true));
        client.on('disconnected', () => setConnected(false));

        client.on('portfolio_snapshot', setData);
        client.on('position_updated', (update) => {
            setData(prev => ({
                ...prev,
                positions: prev.positions.map(p =>
                    p.symbol === update.symbol ? { ...p, ...update } : p
                )
            }));
        });

        client.connect(stream).catch(console.error);

        return () => client.disconnect();
    }, [collectiveId, stream, privateKey]);

    return { connected, data, client: clientRef.current };
    */
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { TradingWebSocketClient };
}
