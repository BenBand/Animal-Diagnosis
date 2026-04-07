/**
 * FarmAI - Smart Livestock Assistant
 * Frontend JavaScript with History and localStorage
 */

class FarmAIChat {
    constructor() {
        this.messages = [];
        this.history = this.loadHistory();
        this.isProcessing = false;
        this.questionCount = this.loadQuestionCount();
        this.requireSignin = this.loadRequireSignin();
        this.signinPromptShown = this.loadSigninPromptShown();  // Track if sign-in prompt has been shown
        this.isLoggedIn = false;
        this.userEmail = null;
        
        // DOM Elements
        this.chatInput = document.getElementById('chatInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.chatMessages = document.getElementById('chatMessages');
        this.historyList = document.getElementById('historyList');
        this.menuToggle = document.getElementById('menuToggle');
        this.sidebar = document.getElementById('sidebar');
        this.closeSidebar = document.getElementById('closeSidebar');
        this.refreshBtn = document.getElementById('refreshBtn');
        this.profileBtn = document.getElementById('profileBtn');
        this.cropDetectionBtn = document.getElementById('cropDetectionBtn');
        this.clearHistoryBtn = document.getElementById('clearHistory');
        
        this.init();
    }

    init() {
        // Event listeners
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
        
        // Sidebar toggles
        this.menuToggle.addEventListener('click', () => this.toggleSidebar(true));
        this.closeSidebar.addEventListener('click', () => this.toggleSidebar(false));
        
        // New chat
        this.refreshBtn.addEventListener('click', () => this.newChat());
        
        // Crop detection button
        if (this.cropDetectionBtn) {
            this.cropDetectionBtn.addEventListener('click', () => this.showCropDetectionModal());
        }
        
        // Clear history
        this.clearHistoryBtn.addEventListener('click', () => this.clearHistory());
        
        // Quick topic buttons
        document.querySelectorAll('.topic-btn, .quick-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const topic = btn.dataset.topic || btn.dataset.question;
                const question = btn.dataset.question || this.getTopicQuestion(topic);
                this.sendMessage(question);
            });
        });
        
        // Load history
        this.renderHistory();
        
        // Check if sign-in was required before refresh
        if (this.requireSignin) {
            this.showSigninModal();
        }
        
        // Update question counter
        this.updateQuestionCounter();
        
        // Check API status
        this.checkAPIStatus();
        
        // Check user session
        this.checkUserSession();
        
        // Offline detection
        this.setupOfflineDetection();
    }

    async checkUserSession() {
        try {
            const response = await fetch('/api/user');
            const data = await response.json();
            if (data.logged_in) {
                this.isLoggedIn = true;
                this.userEmail = data.email;
                this.questionCount = data.question_count;
                this.updateUserDisplay();
                this.updateQuestionCounter();
            }
        } catch (error) {
            console.error('Error checking user session:', error);
        }
    }

    setupOfflineDetection() {
        // Listen for online/offline events
        window.addEventListener('online', () => this.handleOnlineStatus(true));
        window.addEventListener('offline', () => this.handleOnlineStatus(false));
        
        // Initial check
        if (!navigator.onLine) {
            this.handleOnlineStatus(false);
        }
    }

    handleOnlineStatus(isOnline) {
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        
        if (isOnline) {
            statusDot.classList.add('online');
            statusText.textContent = 'AI Ready';
            this.showNotification('You are now online!', 'success');
        } else {
            statusDot.classList.remove('online');
            statusText.textContent = 'Offline';
            this.showNotification('You are offline. Please check your internet connection.', 'error');
        }
    }

    showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${message}</span>
        `;
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => notification.classList.add('show'), 10);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    updateUserDisplay() {
        // Update profile button based on login state
        if (this.profileBtn) {
            if (this.isLoggedIn) {
                // Show logged in state - change icon to indicate logged in
                this.profileBtn.innerHTML = '<i class="fas fa-sign-out-alt"></i>';
                this.profileBtn.title = 'Logout';
                this.profileBtn.style.background = 'var(--primary-light)';
                
                // Remove any existing click listener and add logout handler
                this.profileBtn.onclick = () => this.logout();
            } else {
                // Show logged out state
                this.profileBtn.innerHTML = '<i class="fas fa-user"></i>';
                this.profileBtn.title = 'Login or Register';
                this.profileBtn.style.background = '';
                
                // Remove logout handler and add sign-in modal
                this.profileBtn.onclick = () => this.showSigninModal();
            }
        }
        
        // Remove old user section if exists (we now use profile button)
        const userSection = document.getElementById('userSection');
        if (userSection) userSection.remove();
        
        // Update question counter to show infinity when logged in
        this.updateQuestionCounter();
    }

    async logout() {
        try {
            const response = await fetch('/logout', { method: 'POST' });
            const data = await response.json();
            if (data.success) {
                this.isLoggedIn = false;
                this.userEmail = null;
                this.questionCount = 0;
                this.updateUserDisplay();
                this.updateQuestionCounter();
                this.showNotification('Successfully logged out!', 'success');
            }
        } catch (error) {
            this.showNotification('Error logging out. Please try again.', 'error');
        }
    }

    getTopicQuestion(topic) {
        const questions = {
            cattle: "Tell me about cattle farming",
            poultry: "Tell me about poultry farming",
            sheep: "Tell me about sheep farming",
            goats: "Tell me about goat farming",
            disease: "How to prevent livestock diseases?",
            feed: "What is proper animal nutrition?",
            fish: "Tell me about fish farming",
            crops: "Tell me about crop farming",
            zambia: "Tell me about farming in Zambia"
        };
        return questions[topic] || "Tell me more about farming";
    }

    toggleSidebar(show) {
        if (show) {
            this.sidebar.classList.add('active');
        } else {
            this.sidebar.classList.remove('active');
        }
    }

    newChat() {
        this.messages = [];
        this.chatMessages.innerHTML = `
            <div class="welcome-message">
                <div class="bot-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>Hello! I'm <strong>Bena</strong>, your smart farming assistant. 🐄</p>
                    <p>Ask me about:</p>
                    <ul>
                        <li>Cattle, poultry, sheep, and goats</li>
                        <li>Animal nutrition and feeding</li>
                        <li>Disease prevention and treatment</li>
                        <li>Weather and climate advice</li>
                        <li>Market prices and costs</li>
                    </ul>
                </div>
            </div>
        `;
    }

    // History Management with localStorage
    loadHistory() {
        try {
            const stored = localStorage.getItem('farmai_history');
            return stored ? JSON.parse(stored) : [];
        } catch {
            return [];
        }
    }

    saveHistory() {
        try {
            localStorage.setItem('farmai_history', JSON.stringify(this.history));
        } catch (e) {
            console.warn('Could not save history:', e);
        }
    }

    // Question count persistence with localStorage
    loadQuestionCount() {
        try {
            const stored = localStorage.getItem('farmai_question_count');
            return stored ? parseInt(stored, 10) : 0;
        } catch (e) {
            return 0;
        }
    }

    saveQuestionCount() {
        try {
            localStorage.setItem('farmai_question_count', this.questionCount.toString());
        } catch (e) {
            console.warn('Could not save question count:', e);
        }
    }

    // Require signin persistence with localStorage
    loadRequireSignin() {
        try {
            const stored = localStorage.getItem('farmai_require_signin');
            return stored === 'true';
        } catch (e) {
            return false;
        }
    }
    
    loadSigninPromptShown() {
        try {
            const stored = localStorage.getItem('farmai_signin_prompt_shown');
            return stored === 'true';
        } catch (e) {
            return false;
        }
    }

    saveRequireSignin() {
        try {
            localStorage.setItem('farmai_require_signin', this.requireSignin.toString());
            localStorage.setItem('farmai_signin_prompt_shown', this.signinPromptShown.toString());
        } catch (e) {
            console.warn('Could not save require signin:', e);
        }
    }

    addToHistory(question, answer) {
        const session = {
            id: Date.now(),
            question: question.substring(0, 50) + (question.length > 50 ? '...' : ''),
            preview: answer.substring(0, 60) + (answer.length > 60 ? '...' : ''),
            fullQuestion: question,
            fullAnswer: answer,
            timestamp: new Date().toISOString()
        };
        
        this.history.unshift(session); // Add to beginning
        if (this.history.length > 20) this.history.pop(); // Keep only 20
        
        this.saveHistory();
        this.renderHistory();
    }

    renderHistory() {
        if (this.history.length === 0) {
            this.historyList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-comments"></i>
                    <p>No chat history yet</p>
                </div>
            `;
            return;
        }
        
        this.historyList.innerHTML = this.history.map(item => `
            <div class="history-item" data-id="${item.id}">
                <div class="history-question">${item.question}</div>
                <div class="history-preview">${item.preview}</div>
                <div class="history-time">${this.formatTime(item.timestamp)}</div>
            </div>
        `).join('');
        
        // Add click handlers
        this.historyList.querySelectorAll('.history-item').forEach(item => {
            item.addEventListener('click', () => {
                const id = parseInt(item.dataset.id);
                const session = this.history.find(h => h.id === id);
                if (session) {
                    this.loadSession(session);
                }
            });
        });
    }

    loadSession(session) {
        // Show in chat
        this.messages = [
            { type: 'user', content: session.fullQuestion },
            { type: 'bot', content: session.fullAnswer }
        ];
        this.renderMessages();
        this.toggleSidebar(false); // Close sidebar on mobile
    }

    clearHistory() {
        if (confirm('Clear all chat history?')) {
            this.history = [];
            this.saveHistory();
            this.renderHistory();
        }
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'Just now';
        if (diff < 3600000) return `${Math.floor(diff/60000)}m ago`;
        if (diff < 86400000) return `${Math.floor(diff/3600000)}h ago`;
        return date.toLocaleDateString();
    }

    async sendMessage(text = null) {
        // Block message if sign-in is required
        if (this.requireSignin && this.signinPromptShown) {
            this.showSigninModal();
            return;
        }
        
        // Mark that we've shown the sign-in prompt
        if (this.requireSignin) {
            this.signinPromptShown = true;
        }
        
        if (this.isProcessing) return;
        
        const message = text || this.chatInput.value.trim();
        if (!message) return;
        
        this.isProcessing = true;
        
        // Add user message
        this.messages.push({ type: 'user', content: message });
        this.renderMessages();
        
        // Clear input
        if (!text) this.chatInput.value = '';
        
        // Show typing indicator
        this.showTyping();
        
        try {
            // Call API
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            this.hideTyping();
            
            // Check if sign-in is required
            if (data.require_signin) {
                this.requireSignin = true;
                this.questionCount = data.question_count;
                this.saveRequireSignin();
                this.saveQuestionCount();
                this.showSigninModal();
                // Add bot response
                this.messages.push({ type: 'bot', content: data.answer });
                this.renderMessages();
            } else {
                // Update question count
                if (data.question_count !== undefined) {
                    this.questionCount = data.question_count;
                    this.saveQuestionCount();
                    this.updateQuestionCounter();
                }
                
                // Add bot response
                this.messages.push({ type: 'bot', content: data.answer });
                this.renderMessages();
                
                // Save to history
                this.addToHistory(message, data.answer);
            }
            
        } catch (error) {
            this.hideTyping();
            this.messages.push({ 
                type: 'bot', 
                content: 'Sorry, I encountered an error. Please try again.' 
            });
            this.renderMessages();
            console.error('Error:', error);
        }
        
        this.isProcessing = false;
    }

    showTyping() {
        const typing = document.createElement('div');
        typing.className = 'message bot-message typing';
        typing.id = 'typingIndicator';
        typing.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';
        this.chatMessages.appendChild(typing);
        this.scrollToBottom();
    }

    hideTyping() {
        const typing = document.getElementById('typingIndicator');
        if (typing) typing.remove();
    }

    renderMessages() {
        this.chatMessages.innerHTML = this.messages.map(msg => `
            <div class="message ${msg.type}-message">
                <div class="message-avatar">
                    <i class="fas fa-${msg.type === 'user' ? 'user' : 'robot'}"></i>
                </div>
                <div class="message-content">
                    ${this.formatMessage(msg.content)}
                </div>
            </div>
        `).join('');
        
        this.scrollToBottom();
    }

    formatMessage(content) {
        // Convert markdown-like formatting
        let formatted = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n/g, '<br>')
            .replace(/•/g, '• ')
            .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
        
        // Add list styling
        if (formatted.includes('•')) {
            formatted = formatted.replace(/(•.*?<br>)/g, '<li>$1</li>');
        }
        
        return formatted;
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    // Sign-in modal handling
    showSigninModal() {
        const modal = document.createElement('div');
        modal.className = 'signin-modal';
        modal.innerHTML = `
            <div class="signin-modal-content">
                <button class="close-modal" onclick="this.parentElement.parentElement.remove()">×</button>
                <h3><i class="fas fa-user-plus"></i> Sign In / Register</h3>
                <p>Create an account or sign in to continue asking questions.</p>
                <div class="signin-form">
                    <input type="email" id="signinEmail" placeholder="Enter your email address" />
                    <input type="password" id="signinPassword" placeholder="Enter your password" />
                    <div class="signin-toggle">
                        <button type="button" class="toggle-btn active" data-action="login">Login</button>
                        <button type="button" class="toggle-btn" data-action="register">Register</button>
                    </div>
                    <button id="signinBtn" class="signin-btn">Sign In</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        
        // Handle toggle buttons
        const toggleBtns = modal.querySelectorAll('.toggle-btn');
        const signinBtn = modal.querySelector('#signinBtn');
        let currentAction = 'login';
        
        toggleBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                toggleBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentAction = btn.dataset.action;
                signinBtn.textContent = currentAction === 'register' ? 'Create Account' : 'Sign In';
            });
        });
        
        // Handle sign-in button click
        signinBtn.addEventListener('click', () => this.handleSignin(modal, currentAction));
        modal.querySelector('#signinPassword').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSignin(modal, currentAction);
        });
    }
    
    async handleSignin(modal, action = 'login') {
        console.log('handleSignin called with action:', action);
        
        const email = modal.querySelector('#signinEmail').value.trim();
        const password = modal.querySelector('#signinPassword').value;
        
        console.log('Email:', email);
        console.log('Password length:', password ? password.length : 0);
        
        if (!email || !email.includes('@')) {
            this.showNotification('Please enter a valid email address.', 'error');
            return;
        }
        
        if (!password) {
            this.showNotification('Please enter a password.', 'error');
            return;
        }
        
        this.showNotification('Processing...', 'success');
        
        // Disable button during request
        const signinBtn = modal.querySelector('#signinBtn');
        if (signinBtn) {
            signinBtn.disabled = true;
            signinBtn.textContent = 'Processing...';
        }
        
        try {
            console.log('Sending fetch request to /signin');
            const response = await fetch('/signin', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, action })
            });
            
            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);
            
            const data = await response.json();
            console.log('Response data:', data);
            
            // Re-enable button
            if (signinBtn) {
                signinBtn.disabled = false;
                signinBtn.textContent = action === 'register' ? 'Create Account' : 'Sign In';
            }
            
            if (data.success) {
                this.isLoggedIn = true;
                this.userEmail = data.email;
                this.questionCount = data.question_count;
                this.requireSignin = false;
                this.signinPromptShown = false;  // Reset the flag
                this.saveQuestionCount();
                this.saveRequireSignin();
                this.updateQuestionCounter();
                this.updateUserDisplay();
                modal.remove();
                
                // Clear chat messages for fresh start
                this.messages = [];
                this.renderMessages();
                
                // Scroll to top of chat
                this.chatMessages.scrollTop = 0;
                
                this.messages.push({ 
                    type: 'bot', 
                    content: `✅ Welcome! You've ${action === 'register' ? 'created an account and signed in' : 'signed in'} as ${email}. You now have unlimited questions!` 
                });
                this.renderMessages();
                this.showNotification(data.message, 'success');
            } else {
                this.showNotification(data.message, 'error');
            }
        } catch (error) {
            console.error('Sign in error:', error);
            
            // Re-enable button on error
            const signinBtn = modal.querySelector('#signinBtn');
            if (signinBtn) {
                signinBtn.disabled = false;
                signinBtn.textContent = action === 'register' ? 'Create Account' : 'Sign In';
            }
            
            this.showNotification('Error signing in. Please try again. Error: ' + error.message, 'error');
        }
    }
    
    updateQuestionCounter() {
        const counter = document.getElementById('questionCountText');
        const counterContainer = document.getElementById('questionCounter');
        
        if (this.isLoggedIn) {
            // Show infinity for logged-in users
            if (counter) counter.textContent = '∞';
            if (counterContainer) counterContainer.style.display = 'none';
        } else {
            if (counterContainer) counterContainer.style.display = 'flex';
            if (counter) {
                const remaining = Math.max(0, 5 - this.questionCount);
                counter.textContent = remaining;
            }
        }
    }
    
    // Crop Detection Modal
    async showCropDetectionModal() {
        const modal = document.createElement('div');
        modal.className = 'crop-detection-modal';
        modal.innerHTML = `
            <div class="crop-modal-content">
                <button class="close-modal" onclick="this.parentElement.parentElement.remove()">×</button>
                <h3><i class="fas fa-seedling"></i> Crop Detection</h3>
                <p>Find the best crops for your area based on conditions.</p>
                
                <div class="crop-form">
                    <div class="form-group">
                        <label for="provinceSelect">Select Province</label>
                        <select id="provinceSelect">
                            <option value="">-- Select Province --</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="soilTypeSelect">Soil Type</label>
                        <select id="soilTypeSelect">
                            <option value="sandy">Sandy Soil</option>
                            <option value="sandy_loam">Sandy Loam</option>
                            <option value="loam" selected>Loam</option>
                            <option value="clay_loam">Clay Loam</option>
                            <option value="clay">Clay</option>
                            <option value="black_cotton">Black Cotton</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="rainfallSelect">Rainfall Level</label>
                        <select id="rainfallSelect">
                            <option value="low">Low (0-400mm)</option>
                            <option value="medium" selected>Medium (400-800mm)</option>
                            <option value="high">High (800mm+)</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="weatherTemp">Weather Temperature</label>
                        <select id="weatherTemp">
                            <option value="cool">Cool/Mild</option>
                            <option value="warm" selected>Warm</option>
                            <option value="hot">Hot</option>
                        </select>
                    </div>
                    
                    <button id="detectCropBtn" class="crop-detect-btn">
                        <i class="fas fa-search"></i> Detect Best Crops
                    </button>
                </div>
                
                <div id="cropResults" class="crop-results"></div>
            </div>
        `;
        document.body.appendChild(modal);
        
        // Load provinces
        const provinceSelect = modal.querySelector('#provinceSelect');
        try {
            const response = await fetch('/api/provinces');
            const data = await response.json();
            data.provinces.forEach(province => {
                const option = document.createElement('option');
                option.value = province.id;
                option.textContent = province.name;
                provinceSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error loading provinces:', error);
        }
        
        // Handle detect button click
        const detectBtn = modal.querySelector('#detectCropBtn');
        detectBtn.addEventListener('click', () => this.runCropDetection(modal));
    }
    
    async runCropDetection(modal) {
        const province = modal.querySelector('#provinceSelect').value;
        const soilType = modal.querySelector('#soilTypeSelect').value;
        const rainfall = modal.querySelector('#rainfallSelect').value;
        const weather = {
            temperature: modal.querySelector('#weatherTemp').value,
            humidity: 'moderate'
        };
        
        if (!province) {
            this.showNotification('Please select a province.', 'error');
            return;
        }
        
        const detectBtn = modal.querySelector('#detectCropBtn');
        detectBtn.disabled = true;
        detectBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        
        try {
            const response = await fetch('/api/crop-detection', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ province, soil_type: soilType, rainfall, weather })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayCropResults(modal, data.recommendations);
            } else {
                this.showNotification(data.message || 'Error getting recommendations.', 'error');
            }
        } catch (error) {
            console.error('Crop detection error:', error);
            this.showNotification('Error detecting crops. Please try again.', 'error');
        }
        
        detectBtn.disabled = false;
        detectBtn.innerHTML = '<i class="fas fa-search"></i> Detect Best Crops';
    }
    
    displayCropResults(modal, recommendations) {
        const resultsContainer = modal.querySelector('#cropResults');
        
        if (!recommendations || recommendations.length === 0) {
            resultsContainer.innerHTML = '<p class="no-results">No recommendations found for these conditions.</p>';
            return;
        }
        
        let html = '<h4>Recommended Crops:</h4>';
        recommendations.forEach((rec, index) => {
            const suitabilityColor = rec.suitability >= 80 ? 'green' : rec.suitability >= 60 ? 'orange' : 'red';
            html += `
                <div class="crop-result-card">
                    <div class="crop-result-header">
                        <span class="crop-name">${rec.crop}</span>
                        <span class="crop-suitability" style="color: ${suitabilityColor}">${rec.suitability}%</span>
                    </div>
                    <div class="crop-result-details">
                        <p><strong>Planting Season:</strong> ${rec.season}</p>
                        <p><strong>Expected Yield:</strong> ${rec.yield}</p>
                        <p><strong>Tips:</strong> ${rec.planting_tips}</p>
                    </div>
                </div>
            `;
        });
        
        resultsContainer.innerHTML = html;
    }
    
    async checkAPIStatus() {
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            statusDot.classList.add('online');
            statusText.textContent = 'AI Ready';
        } catch {
            statusDot.classList.remove('online');
            statusText.textContent = 'Offline';
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    window.chat = new FarmAIChat();
});