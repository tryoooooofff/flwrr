// ========== data_manager.js ==========
// 数据管理类 - 处理游戏数据的云端保存

class DataManager {
    constructor() {
        this.githubToken = null;
        this.gistId = null;
        this.dataCache = {};
        this.autoSaveInterval = 20000; // 20秒自动保存
        this.lastSaveTime = 0;

        // 尝试加载保存的配置
        this.loadConfig();
    }

    // 加载配置
    loadConfig() {
        try {
            const saved = localStorage.getItem('flwrr_config');
            if (saved) {
                const config = JSON.parse(saved);
                this.githubToken = config.githubToken;
                this.gistId = config.gistId;
            }
        } catch (e) {
            console.log('没有保存的配置');
        }
    }

    // 保存配置
    saveConfig() {
        const config = {
            githubToken: this.githubToken,
            gistId: this.gistId
        };
        localStorage.setItem('flwrr_config', JSON.stringify(config));
    }

    // 设置 GitHub Token
    setGithubToken(token) {
        this.githubToken = token;
        this.saveConfig();
    }

    // 创建新的 Gist 用于保存游戏数据
    async createGist() {
        if (!this.githubToken) {
            throw new Error('请先设置 GitHub Token');
        }

        const data = {
            description: 'Flwrr 游戏存档',
            public: false,
            files: {
                'flwrr_save.json': {
                    content: JSON.stringify({
                        version: '1.0',
                        lastSave: new Date().toISOString(),
                        players: {}
                    }, null, 2)
                }
            }
        };

        try {
            const response = await fetch('https://api.github.com/gists', {
                method: 'POST',
                headers: {
                    'Authorization': `token ${this.githubToken}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            this.gistId = result.id;
            this.saveConfig();

            console.log('✅ Gist 创建成功！ID:', this.gistId);
            return result.id;
        } catch (error) {
            console.error('❌ 创建 Gist 失败:', error);
            throw error;
        }
    }

    // 保存玩家数据到 Gist
    async savePlayerData(playerId, playerData) {
        if (!this.gistId || !this.githubToken) {
            console.log('请先创建 Gist');
            return false;
        }

        try {
            // 先获取当前 Gist 内容
            const getResponse = await fetch(`https://api.github.com/gists/${this.gistId}`, {
                headers: {
                    'Authorization': `token ${this.githubToken}`
                }
            });

            const gist = await getResponse.json();
            let currentData = {};

            if (gist.files && gist.files['flwrr_save.json']) {
                currentData = JSON.parse(gist.files['flwrr_save.json'].content);
            }

            // 更新玩家数据
            if (!currentData.players) currentData.players = {};
            currentData.players[playerId] = {
                ...playerData,
                lastUpdate: new Date().toISOString()
            };
            currentData.lastSave = new Date().toISOString();

            // 更新 Gist
            const updateData = {
                files: {
                    'flwrr_save.json': {
                        content: JSON.stringify(currentData, null, 2)
                    }
                }
            };

            const updateResponse = await fetch(`https://api.github.com/gists/${this.gistId}`, {
                method: 'PATCH',
                headers: {
                    'Authorization': `token ${this.githubToken}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updateData)
            });

            const result = await updateResponse.json();
            console.log('✅ 数据保存成功！');
            return true;
        } catch (error) {
            console.error('❌ 保存失败:', error);
            return false;
        }
    }

    // 加载玩家数据
    async loadPlayerData(playerId) {
        if (!this.gistId) return null;

        try {
            const response = await fetch(`https://api.github.com/gists/${this.gistId}`, {
                headers: {
                    'Authorization': `token ${this.githubToken}`
                }
            });

            const gist = await response.json();

            if (gist.files && gist.files['flwrr_save.json']) {
                const data = JSON.parse(gist.files['flwrr_save.json'].content);
                return data.players?.[playerId] || null;
            }

            return null;
        } catch (error) {
            console.error('❌ 加载失败:', error);
            return null;
        }
    }

    // 获取所有玩家数据
    async getAllPlayersData() {
        if (!this.gistId) return {};

        try {
            const response = await fetch(`https://api.github.com/gists/${this.gistId}`, {
                headers: {
                    'Authorization': `token ${this.githubToken}`
                }
            });

            const gist = await response.json();

            if (gist.files && gist.files['flwrr_save.json']) {
                const data = JSON.parse(gist.files['flwrr_save.json'].content);
                return data.players || {};
            }

            return {};
        } catch (error) {
            console.error('❌ 加载失败:', error);
            return {};
        }
    }
}

// 导出单例
export const dataManager = new DataManager();