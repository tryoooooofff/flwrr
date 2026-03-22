// server.js - 在 Render 上运行
import { WebSocketServer } from 'ws';
import { v4 as uuidv4 } from 'uuid';

const PORT = process.env.PORT || 10000;
const wss = new WebSocketServer({ port: PORT });

console.log(`🚀 WebSocket 服务器运行在端口 ${PORT}`);

// 游戏房间管理
const rooms = new Map();

class GameRoom {
    constructor(roomCode, biome = "Plain") {
        this.code = roomCode;
        this.biome = biome;
        this.players = new Map();      // playerId -> Player
        this.enemies = [];
        this.drops = [];
        this.lastUpdate = Date.now();
        this.worldSize = 10000;
        this.spawnTimer = 0;

        // 启动游戏循环 (20fps)
        this.interval = setInterval(() => this.update(), 50);
        console.log(`🏠 房间 ${roomCode} 创建 (${biome})`);
    }

    update() {
        const now = Date.now();
        const dt = Math.min(0.05, (now - this.lastUpdate) / 1000);
        this.lastUpdate = now;

        // 1. 处理所有玩家输入（服务器权威移动）
        for (const player of this.players.values()) {
            if (player.inputs.length > 0) {
                const input = player.inputs[player.inputs.length - 1];

                // 服务器计算移动
                const screenCenterX = 400;
                const screenCenterY = 300;
                const dx = input.mouseX - screenCenterX;
                const dy = input.mouseY - screenCenterY;
                const dist = Math.hypot(dx, dy);

                if (dist > 30) {
                    const speed = 150;
                    player.x += (dx / dist) * speed * dt;
                    player.y += (dy / dist) * speed * dt;
                }

                // 边界检查
                player.x = Math.max(20, Math.min(this.worldSize - 20, player.x));
                player.y = Math.max(20, Math.min(this.worldSize - 20, player.y));
                player.inputs = [];
            }
        }

        // 2. 简单敌人AI
        for (let i = 0; i < this.enemies.length; i++) {
            const enemy = this.enemies[i];

            // 找最近的玩家
            let target = null;
            let minDist = Infinity;
            for (const player of this.players.values()) {
                if (player.dead) continue;
                const dist = Math.hypot(enemy.x - player.x, enemy.y - player.y);
                if (dist < minDist) {
                    minDist = dist;
                    target = player;
                }
            }

            // 敌人移动
            if (target && minDist < 400) {
                const dx = target.x - enemy.x;
                const dy = target.y - enemy.y;
                const dist = Math.hypot(dx, dy);
                if (dist > 0) {
                    enemy.x += (dx / dist) * enemy.speed * dt;
                    enemy.y += (dy / dist) * enemy.speed * dt;
                }
            }

            // 边界检查
            enemy.x = Math.max(20, Math.min(this.worldSize - 20, enemy.x));
            enemy.y = Math.max(20, Math.min(this.worldSize - 20, enemy.y));
        }

        // 3. 生成敌人
        if (this.enemies.length < 30 && Math.random() < 0.05) {
            const players = Array.from(this.players.values()).filter(p => !p.dead);
            if (players.length > 0) {
                const p = players[Math.floor(Math.random() * players.length)];
                const angle = Math.random() * Math.PI * 2;
                const dist = 400 + Math.random() * 200;

                this.enemies.push({
                    id: uuidv4(),
                    type: ["Spider", "Bee", "Ladybug"][Math.floor(Math.random() * 3)],
                    x: p.x + Math.cos(angle) * dist,
                    y: p.y + Math.sin(angle) * dist,
                    health: 100,
                    maxHealth: 100,
                    speed: 50
                });
            }
        }

        // 4. 广播状态
        this.broadcast();
    }

    broadcast() {
        const state = {
            type: 'game_state',
            players: Array.from(this.players.values()).map(p => ({
                id: p.id,
                x: p.x,
                y: p.y,
                health: p.health,
                dead: p.dead
            })),
            enemies: this.enemies.map(e => ({
                id: e.id,
                type: e.type,
                x: e.x,
                y: e.y,
                health: e.health,
                maxHealth: e.maxHealth
            })),
            drops: this.drops
        };

        const msg = JSON.stringify(state);
        for (const player of this.players.values()) {
            if (player.ws.readyState === 1) {
                player.ws.send(msg);
            }
        }

        this.drops = [];
    }

    stop() {
        clearInterval(this.interval);
    }
}

// WebSocket 连接处理
wss.on('connection', (ws, req) => {
    const url = new URL(req.url, `http://${req.headers.host}`);
    const roomCode = url.searchParams.get('room') || 'default';
    const playerName = url.searchParams.get('name') || 'Player';

    // 获取或创建房间
    if (!rooms.has(roomCode)) {
        rooms.set(roomCode, new GameRoom(roomCode));
    }
    const room = rooms.get(roomCode);

    const playerId = uuidv4();
    const player = {
        id: playerId,
        name: playerName,
        ws: ws,
        x: 5000,
        y: 5000,
        health: 100,
        dead: false,
        inputs: []
    };

    room.players.set(playerId, player);
    console.log(`✅ 玩家 ${playerName} (${playerId}) 加入房间 ${roomCode}`);

    // 发送初始化消息
    ws.send(JSON.stringify({
        type: 'init',
        playerId: playerId,
        worldSize: room.worldSize,
        players: Array.from(room.players.values()).map(p => ({
            id: p.id,
            name: p.name,
            x: p.x,
            y: p.y,
            health: p.health
        })),
        enemies: room.enemies
    }));

    // 通知其他玩家有新玩家加入
    for (const p of room.players.values()) {
        if (p.id !== playerId && p.ws.readyState === 1) {
            p.ws.send(JSON.stringify({
                type: 'player_joined',
                playerId: playerId,
                name: playerName,
                x: player.x,
                y: player.y
            }));
        }
    }

    // 处理消息
    ws.on('message', (data) => {
        try {
            const msg = JSON.parse(data);

            switch(msg.type) {
                case 'input':
                    player.inputs.push({
                        mouseX: msg.mouseX,
                        mouseY: msg.mouseY,
                        seq: msg.seq
                    });
                    break;

                case 'chat':
                    // 广播聊天消息
                    for (const p of room.players.values()) {
                        if (p.ws.readyState === 1) {
                            p.ws.send(JSON.stringify({
                                type: 'chat',
                                sender: playerName,
                                text: msg.text,
                                time: Date.now()
                            }));
                        }
                    }
                    break;
            }
        } catch (e) {
            console.error('消息解析错误:', e);
        }
    });

    // 断开连接
    ws.on('close', () => {
        console.log(`❌ 玩家 ${playerName} 离开房间 ${roomCode}`);
        room.players.delete(playerId);

        // 通知其他玩家
        for (const p of room.players.values()) {
            if (p.ws.readyState === 1) {
                p.ws.send(JSON.stringify({
                    type: 'player_left',
                    playerId: playerId
                }));
            }
        }

        if (room.players.size === 0) {
            room.stop();
            rooms.delete(roomCode);
            console.log(`🏠 房间 ${roomCode} 已关闭`);
        }
    });
});