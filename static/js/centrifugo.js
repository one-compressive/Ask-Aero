(function() {
    'use strict';

    const wsUrl = document.getElementById('centrifugo-ws-url')?.dataset.url;
    const channel = document.getElementById('centrifugo-channel')?.dataset.channel;

    if (!wsUrl || !channel) {
        return;
    }

    let client = null;
    let subscription = null;

    try {
        client = new Centrifuge(wsUrl, {
            token: ""
        });

        client.on('connected', function(ctx) {
            console.log('Connected to Centrifugo');
        });

        client.on('disconnected', function(ctx) {
            console.log('Disconnected from Centrifugo');
        });

        subscription = client.getSubscription(channel);

        if (!subscription) {
            subscription = client.newSubscription(channel);

            subscription.on('publication', function(ctx) {
                const answerData = ctx.data;
                addAnswerToPage(answerData);
            });

            subscription.subscribe();
        }

        client.connect();
    } catch (error) {
        console.error('Centrifugo connection error:', error);
    }

    function addAnswerToPage(answerData) {
        const answersContainer = document.querySelector('.answers-container');
        if (!answersContainer) {
            return;
        }

        const answerHtml = `
            <article class="post-item ${answerData.is_correct ? 'correct-answer' : ''}">
                <div class="left-subsection">
                    ${answerData.author_avatar
                        ? `<img src="${answerData.author_avatar}" alt="${answerData.author}" class="img-small">`
                        : `<img src="/static/img/default-avatar.jpg" alt="Default" class="img-small">`
                    }
                    <div class="vote">
                        <span class="count" id="answer-${answerData.id}-score">${answerData.score || 0}</span>
                        <div class="vote-buttons">
                            <button class="upvote" onclick="voteAnswer(${answerData.id}, 'like')">&#9650;</button>
                            <button class="downvote" onclick="voteAnswer(${answerData.id}, 'dislike')">&#9660;</button>
                        </div>
                    </div>
                </div>
                <div class="right-subsection">
                    <div class="post-text">
                        <p>${escapeHtml(answerData.text)}</p>
                    </div>
                    <div class="bottom-right-subsection answer-meta-actions">
                        <span class="author-info">Answered by <a href="#">${escapeHtml(answerData.author)}</a> on ${formatDate(answerData.created_at)}</span>
                    </div>
                </div>
            </article>
        `;

        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = answerHtml;
        const newAnswer = tempDiv.firstElementChild;

        const firstAnswer = answersContainer.querySelector('.post-item');
        if (firstAnswer) {
            firstAnswer.insertAdjacentElement('beforebegin', newAnswer);
        } else {
            answersContainer.appendChild(newAnswer);
        }

        updateAnswersCount();
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleString('ru-RU');
    }

    function updateAnswersCount() {
        const answers = document.querySelectorAll('.post-item');
        const count = answers.length - 1;
        const header = document.querySelector('.answers-header h2');
        if (header) {
            header.textContent = `${count} Answer${count !== 1 ? 's' : ''}`;
        }
    }

    window.addEventListener('beforeunload', function() {
        if (subscription) {
            subscription.unsubscribe();
        }
        if (client) {
            client.disconnect();
        }
    });
})();
