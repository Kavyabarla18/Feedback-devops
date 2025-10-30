# Create HTML template for Flask
html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feedback Collection System - Backend</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .stats-bar {
            display: flex;
            justify-content: space-around;
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            margin-top: 20px;
            border-radius: 10px;
        }

        .stat-item {
            text-align: center;
        }

        .stat-number {
            font-size: 2em;
            font-weight: bold;
        }

        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }

        .content {
            padding: 40px;
        }

        .form-section {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 40px;
        }

        .form-section h2 {
            color: #333;
            margin-bottom: 25px;
            font-size: 1.8em;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #495057;
            font-size: 1em;
        }

        input, textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            transition: all 0.3s ease;
        }

        input:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        textarea {
            min-height: 120px;
            resize: vertical;
        }

        .char-counter {
            text-align: right;
            font-size: 0.85em;
            color: #6c757d;
            margin-top: 5px;
        }

        .submit-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 18px 40px;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }

        .submit-btn:active {
            transform: translateY(0);
        }

        .submit-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .alert {
            padding: 15px 20px;
            margin-bottom: 25px;
            border-radius: 10px;
            font-weight: 500;
            display: none;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 2px solid #c3e6cb;
        }

        .alert-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 2px solid #f5c6cb;
        }

        .feedback-list-section h2 {
            color: #333;
            margin-bottom: 25px;
            font-size: 1.8em;
        }

        .feedback-grid {
            display: grid;
            gap: 20px;
        }

        .feedback-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
            transition: all 0.3s ease;
            position: relative;
        }

        .feedback-card:hover {
            transform: translateX(10px);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }

        .feedback-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }

        .feedback-meta {
            display: flex;
            align-items: center;
            gap: 15px;
            font-size: 0.9em;
            color: #6c757d;
        }

        .feedback-id {
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.85em;
        }

        .feedback-author {
            font-weight: 600;
            color: #495057;
        }

        .feedback-time {
            color: #6c757d;
        }

        .feedback-content {
            font-size: 1.05em;
            line-height: 1.6;
            color: #343a40;
            margin-top: 10px;
        }

        .no-feedback {
            text-align: center;
            padding: 60px 20px;
            color: #6c757d;
        }

        .no-feedback-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }

        .no-feedback-text {
            font-size: 1.3em;
            margin-bottom: 10px;
        }

        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 0.6s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8em;
            }

            .stats-bar {
                flex-direction: column;
                gap: 15px;
            }

            .content {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💬 Feedback Collection System</h1>
            <p>Powered by Flask Backend API</p>
            <div class="stats-bar">
                <div class="stat-item">
                    <div class="stat-number">{{ total_count }}</div>
                    <div class="stat-label">Total Feedback</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{{ feedback_list|length }}</div>
                    <div class="stat-label">Recent Entries</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="live-count">0</div>
                    <div class="stat-label">Live Sessions</div>
                </div>
            </div>
        </div>

        <div class="content">
            <div class="form-section">
                <h2>📝 Share Your Feedback</h2>
                <form id="feedbackForm">
                    <div class="form-group">
                        <label for="name">👤 Your Name (Optional)</label>
                        <input type="text" 
                               id="name" 
                               name="name" 
                               placeholder="Enter your name"
                               maxlength="100">
                    </div>
                    
                    <div class="form-group">
                        <label for="email">📧 Email Address (Optional)</label>
                        <input type="email" 
                               id="email" 
                               name="email" 
                               placeholder="your.email@example.com"
                               maxlength="100">
                    </div>
                    
                    <div class="form-group">
                        <label for="feedback">💭 Your Feedback *</label>
                        <textarea id="feedback" 
                                  name="feedback" 
                                  placeholder="Please share your thoughts, suggestions, or feedback..."
                                  required
                                  maxlength="1000"></textarea>
                        <div class="char-counter">
                            <span id="charCount">0</span> / 1000 characters
                        </div>
                    </div>
                    
                    <button type="submit" class="submit-btn" id="submitBtn">
                        Submit Feedback
                    </button>
                </form>
            </div>
            
            <div id="message"></div>
            
            <div class="feedback-list-section">
                <h2>📋 Recent Feedback</h2>
                <div class="feedback-grid" id="feedbackGrid">
                    {% if feedback_list %}
                        {% for feedback in feedback_list %}
                        <div class="feedback-card">
                            <div class="feedback-header">
                                <div class="feedback-meta">
                                    <span class="feedback-id">#{{ feedback.id }}</span>
                                    <span class="feedback-author">{{ feedback.name }}</span>
                                    {% if feedback.email %}
                                    <span class="feedback-email">{{ feedback.email }}</span>
                                    {% endif %}
                                </div>
                                <span class="feedback-time">🕒 {{ feedback.timestamp[:19] }}</span>
                            </div>
                            <div class="feedback-content">{{ feedback.feedback }}</div>
                        </div>
                        {% endfor %}
                    {% else %}
                        <div class="no-feedback">
                            <div class="no-feedback-icon">📭</div>
                            <div class="no-feedback-text">No feedback yet</div>
                            <p>Be the first to share your thoughts!</p>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <script>
        // Character counter
        const feedbackTextarea = document.getElementById('feedback');
        const charCount = document.getElementById('charCount');
        
        feedbackTextarea.addEventListener('input', function() {
            charCount.textContent = this.value.length;
        });

        // Form submission
        document.getElementById('feedbackForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const originalText = submitBtn.innerHTML;
            
            // Disable button and show loading
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="loading"></span> Submitting...';
            
            const formData = {
                name: document.getElementById('name').value.trim(),
                email: document.getElementById('email').value.trim(),
                feedback: document.getElementById('feedback').value.trim()
            };
            
            try {
                const response = await fetch('/api/feedback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                const messageDiv = document.getElementById('message');
                
                if (response.ok) {
                    messageDiv.innerHTML = 
                        '<div class="alert alert-success" style="display: block;">✅ ' + result.message + '</div>';
                    document.getElementById('feedbackForm').reset();
                    charCount.textContent = '0';
                    
                    // Reload page after 2 seconds to show new feedback
                    setTimeout(() => {
                        location.reload();
                    }, 2000);
                } else {
                    throw new Error(result.error || 'Unknown error occurred');
                }
            } catch (error) {
                document.getElementById('message').innerHTML = 
                    '<div class="alert alert-error" style="display: block;">❌ Error: ' + error.message + '</div>';
                
                // Re-enable button
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        });

        // Live counter animation (simulated)
        let count = 0;
        setInterval(() => {
            count = Math.floor(Math.random() * 10) + 1;
            document.getElementById('live-count').textContent = count;
        }, 3000);

        // Auto-hide alerts after 5 seconds
        setTimeout(() => {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => {
                if (alert.style.display === 'block') {
                    alert.style.display = 'none';
                }
            });
        }, 5000);
    </script>
</body>
</html>
'''

with open(f"{backend_dir}/app/templates/index.html", 'w', encoding='utf-8') as f:
    f.write(html_template)

print("✅ HTML template created: app/templates/index.html")
