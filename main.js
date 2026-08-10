// Windear Landing Page — Main JavaScript

(function () {
  // Global modal opener for inline onclick backup
  window.openWindearSurvey = function (e) {
    if (e && e.preventDefault) e.preventDefault();
    var surveyModal = document.getElementById('survey-modal');
    if (surveyModal) {
      surveyModal.style.setProperty('display', 'flex', 'important');
      surveyModal.style.setProperty('opacity', '1', 'important');
      surveyModal.style.setProperty('pointer-events', 'auto', 'important');
      surveyModal.classList.add('active');
      surveyModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }
  };

  window.closeWindearSurvey = function () {
    var surveyModal = document.getElementById('survey-modal');
    if (surveyModal) {
      surveyModal.style.setProperty('display', 'none', 'important');
      surveyModal.style.setProperty('opacity', '0', 'important');
      surveyModal.style.setProperty('pointer-events', 'none', 'important');
      surveyModal.classList.remove('active');
      surveyModal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';

      // Reset back to form view after close animation completes
      setTimeout(function () {
        var formView = document.getElementById('modal-form-view');
        var thankYouView = document.getElementById('modal-thankyou-view');
        if (formView) formView.style.display = 'flex';
        if (thankYouView) thankYouView.style.display = 'none';
      }, 300);
    }
  };

  // Top-Level Global Chatbot Toggle Function
  window.toggleWindearChatbot = function (e) {
    if (e && e.preventDefault) e.preventDefault();
    var chatWin = document.getElementById('chatbot-window');
    var togBtn = document.getElementById('chatbot-toggle-btn');
    if (!chatWin) return;

    var isHidden = chatWin.classList.contains('hidden') || chatWin.style.display === 'none';
    if (isHidden) {
      chatWin.classList.remove('hidden');
      chatWin.classList.add('active');
      chatWin.style.display = 'flex';
      if (togBtn) {
        var iconOpen = togBtn.querySelector('.chat-icon-open');
        var iconClose = togBtn.querySelector('.chat-icon-close');
        if (iconOpen) iconOpen.style.display = 'none';
        if (iconClose) iconClose.style.display = 'block';
      }
      if (window.triggerGreetingIfEmpty) {
        window.triggerGreetingIfEmpty();
      }
    } else {
      chatWin.classList.add('hidden');
      chatWin.classList.remove('active');
      chatWin.style.display = 'none';
      if (togBtn) {
        var iconOpen = togBtn.querySelector('.chat-icon-open');
        var iconClose = togBtn.querySelector('.chat-icon-close');
        if (iconOpen) iconOpen.style.display = 'block';
        if (iconClose) iconClose.style.display = 'none';
      }
    }
  };

  function initWindear() {
    /* ==========================================================================
       1. FAQ ACCORDION HANDLER
       ========================================================================== */
    var faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(function (item) {
      var questionBtn = item.querySelector('.faq-question');
      if (!questionBtn) return;
      
      questionBtn.addEventListener('click', function () {
        var isActive = item.classList.contains('active');
        
        // Close all other accordion items
        faqItems.forEach(function (otherItem) {
          otherItem.classList.remove('active');
          var btn = otherItem.querySelector('.faq-question');
          if (btn) btn.setAttribute('aria-expanded', 'false');
        });

        // Toggle current item
        if (!isActive) {
          item.classList.add('active');
          questionBtn.setAttribute('aria-expanded', 'true');
        }
      });
    });

    /* ==========================================================================
       2. INTERACTIVE DEMO AUDIO SIMULATOR (Web Audio API)
       ========================================================================== */
    var btnPlayChunk = document.getElementById('btn-play-chunk');
    var btnPlayFull = document.getElementById('btn-play-full');
    var soundwave = document.getElementById('soundwave');
    var chunkWord = document.getElementById('chunk-word');
    var demoStatus = document.getElementById('demo-status-text');

    var audioCtx = null;

    function initAudio() {
      if (!audioCtx) {
        var AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) {
          audioCtx = new AudioContext();
        }
      }
    }

    function playSynthesizedSpeech(durationMs, pitchFreq, labelText) {
      initAudio();
      if (soundwave) soundwave.classList.add('playing');
      if (chunkWord) chunkWord.classList.add('active-playing');
      if (demoStatus) demoStatus.textContent = labelText;

      if (audioCtx) {
        try {
          var osc = audioCtx.createOscillator();
          var gain = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(pitchFreq, audioCtx.currentTime);
          
          osc.frequency.exponentialRampToValueAtTime(pitchFreq * 1.3, audioCtx.currentTime + durationMs / 2000);
          osc.frequency.exponentialRampToValueAtTime(pitchFreq * 0.9, audioCtx.currentTime + durationMs / 1000);

          gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + durationMs / 1000);

          osc.connect(gain);
          gain.connect(audioCtx.destination);

          osc.start();
          osc.stop(audioCtx.currentTime + durationMs / 1000);
        } catch (e) {
          console.warn('Audio Context play error:', e);
        }
      }

      setTimeout(function () {
        if (soundwave) soundwave.classList.remove('playing');
        if (chunkWord) chunkWord.classList.remove('active-playing');
      }, durationMs);
    }

    if (btnPlayChunk) {
      btnPlayChunk.addEventListener('click', function () {
        playSynthesizedSpeech(1200, 320, '🔊 BƯỚC 3: Đang phát chậm cụm từ "piece of cake" (Mỹ, Anh, Úc)... Đã thấu hiểu!');
      });
    }

    if (btnPlayFull) {
      btnPlayFull.addEventListener('click', function () {
        playSynthesizedSpeech(2200, 440, '⚡ BƯỚC 4: Đang phát câu gốc tốc độ tự nhiên... Bạn đã nghe ra 100%!');
      });
    }

    /* ==========================================================================
       3. STICKY MOBILE CTA DISPLAY ON SCROLL
       ========================================================================== */
    var mobileSticky = document.getElementById('mobile-sticky');
    var heroSection = document.getElementById('hero');

    function checkStickyCTA() {
      if (!mobileSticky || !heroSection) return;
      var heroBottom = heroSection.getBoundingClientRect().bottom;
      if (heroBottom < 100) {
        mobileSticky.classList.add('visible');
      } else {
        mobileSticky.classList.remove('visible');
      }
    }

    window.addEventListener('scroll', checkStickyCTA, { passive: true });
    checkStickyCTA();

    /* ==========================================================================
       4. SMOOTH SCROLL FOR NON-MODAL ANCHOR LINKS
       ========================================================================== */
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        if (this.classList.contains('js-open-survey-modal')) {
          e.preventDefault();
          window.openWindearSurvey(e);
          return;
        }

        var targetId = this.getAttribute('href');
        if (targetId === '#' || targetId === '#survey') return;
        
        var targetEl = document.querySelector(targetId);
        if (targetEl) {
          e.preventDefault();
          targetEl.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });

    /* ==========================================================================
       5. SURVEY MODAL EVENT LISTENERS & VIEW SWITCHING
       ========================================================================== */
    var surveyModal = document.getElementById('survey-modal');
    var modalCloseBtn = document.getElementById('modal-close');
    var modalSkipBtn = document.getElementById('modal-skip-btn');
    var btnConfirmSurvey = document.getElementById('btn-confirm-survey');
    var btnCloseThankYou = document.getElementById('btn-close-thankyou');
    var formView = document.getElementById('modal-form-view');
    var thankYouView = document.getElementById('modal-thankyou-view');
    var ctaModalTriggers = document.querySelectorAll('.js-open-survey-modal');

    ctaModalTriggers.forEach(function (btn) {
      btn.addEventListener('click', window.openWindearSurvey);
    });

    if (modalCloseBtn) {
      modalCloseBtn.addEventListener('click', window.closeWindearSurvey);
    }

    if (modalSkipBtn) {
      modalSkipBtn.addEventListener('click', function () {
        window.closeWindearSurvey();
        var methodSection = document.getElementById('method');
        if (methodSection) {
          methodSection.scrollIntoView({ behavior: 'smooth' });
        }
      });
    }

    // Native Form Submission Listener (Delegated to Unified Single Direct Submit)
    var nativeForm = document.getElementById('native-customer-form');
    if (nativeForm) {
      nativeForm.addEventListener('submit', function (e) {
        if (e && e.preventDefault) e.preventDefault();
        if (window.submitWaitlistFormDirect) {
          window.submitWaitlistFormDirect(e);
        }
      });
    }

        // Đồng bộ thời gian thực cho trang Admin
        try {
          const bc = new BroadcastChannel('windear_crm_channel');
          bc.postMessage({ type: 'CUSTOMERS_UPDATED' });
        } catch(e) {}
      });
    }

    // Auto-sync any submissions filled prior to starting server.py
    try {
      var prevSavedList = JSON.parse(localStorage.getItem('windear_customers_data') || '[]');
      if (prevSavedList.length > 0) {
        prevSavedList.forEach(function (entry) {
          fetch('/api/save-customer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(entry)
          }).then(function() {
            console.log('✅ Đã đồng bộ dữ liệu điền trước đó vào customers.md:', entry);
          });
        });
        localStorage.removeItem('windear_customers_data');
      }
    } catch(e) {}

    // Close modal from Thank-You Screen
    if (btnCloseThankYou) {
      btnCloseThankYou.addEventListener('click', window.closeWindearSurvey);
    }

    if (surveyModal) {
      surveyModal.addEventListener('click', function (e) {
        if (e.target === surveyModal) {
          window.closeWindearSurvey();
        }
      });
    }

    window.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && surveyModal && surveyModal.classList.contains('active')) {
        window.closeWindearSurvey();
      }
    });

    /* ==========================================================================
       4. WINDEAR SALES CHATBOT LOGIC (SALES_SCRIPT.MD)
       ========================================================================== */
    var toggleBtn = document.getElementById('chatbot-toggle-btn');
    var chatWindow = document.getElementById('chatbot-window');
    var closeBtn = document.getElementById('chatbot-close-btn');
    var messagesContainer = document.getElementById('chatbot-messages');
    var inputField = document.getElementById('chatbot-input');
    var sendBtn = document.getElementById('chatbot-send-btn');
    var quickRepliesContainer = document.getElementById('chatbot-quick-replies');

    var isInitialized = false;

    // Sales Knowledge Base matching sales_script.md
    var botScript = {
      greeting: "Chào bạn nha! 👋 Mình là Trợ lý Windear AI đây. Có phải bạn đang gặp tình trạng 'biết từ vựng nhưng người bản xứ nói nhanh là nghe trôi tuột chữ' không? Bạn cần tư vấn hay có thắc mắc gì cứ hỏi mình thoải mái nhé!",
      
      answers: {
        free: "Yên tâm 100% nha bạn ơi! Bản Tiêu chuẩn của Windear cam kết MIỄN PHÍ hoàn toàn trọn đời cho mọi tính năng luyện nghe cốt lõi. Không có gài gắm chi phí ẩn hay bắt buộc nạp tiền gì hết nha!",
        lost: "Luyện tốt luôn bạn nha! Windear chia nhỏ câu thoại thành từng cụm 2-3 từ ngắn, hỗ trợ dịch nghĩa từng từ và tùy chỉnh tốc độ từ 0.5x. Dù bạn mất gốc thì tai vẫn tự nhận diện được âm thanh dễ dàng trước khi ghép lại cả câu.",
        time: "Siêu hiệu quả luôn! Windear thiết kế bài luyện dạng micro-learning chỉ 5 phút/ngày. Nhờ thuật toán tập trung bóc tách đúng 'từ bị dính bẫy âm thanh', 5 phút trên Windear hiệu quả hơn 45 phút bạn tự bơi xem phim ngoài kia đấy!",
        diff: "eJOY/Mochi rất hay để học từ vựng hay giải trí, ELSA mạnh về sửa phát âm NÓI. Còn Windear tập trung 100% trị dứt điểm lỗi 'NGHE trôi tuột chữ' đời thực bằng thuật toán xẻ nhỏ audio 4 giọng đọc. Ngắn gọn, hiệu quả và Miễn Phí 100%!",
        accents: "Có đủ 4 giọng luôn nha! Windear tích hợp audio chuẩn 4 quốc gia: Mỹ 🇺🇸, Anh 🇬🇧, Úc 🇦🇺 và Canada 🇨🇦. Giúp tai bạn quen phản xạ đa giọng, ra đời thực gặp giọng lạ vẫn bắt kịp dễ dàng.",
        method: "Rất đơn giản: Bước 1 Chọn chủ đề ưa thích -> Bước 2 Nghe xẻ nhỏ audio đoán từ ẩn -> Bước 3 Ráp lại cả câu tăng tốc độ (1.0x -> 2.0x) -> Bước 4 Ôn tập giữ Streak 7 ngày. Máy lo hết, bạn chỉ cần 5 phút trải nghiệm!",
        pro: "Gói Pro là tính năng nâng cao dành cho bạn nào muốn tải file audio/video cá nhân lên để app bóc tách riêng. Hiện tại Windear đang tặng 1 tháng Pro miễn phí cho những bạn đăng ký sớm trong Danh sách chờ (Waitlist) đó ạ!",
        streak: "Bạn chỉ cần hoàn thành 1 bài luyện 5 phút mỗi ngày, hệ thống sẽ tự động ghi nhận Streak và thưởng huy hiệu tiến độ cho bạn nha!",
        waitlist: "Đăng ký Form Waitlist hôm nay bạn nhận ngay: 🎁 1 Tháng sử dụng Windear Pro VIP miễn phí khi ra mắt + 📚 Ebook 'Bí kíp nảy số tai tiếng Anh trong 7 ngày' độc quyền!",
        buy: "Thật ra không cần tốn tiền triệu hay ngồi gõ chép chính tả mỏi tay đâu bạn ơi! Trải nghiệm ngay phương pháp xẻ nhỏ audio 4 bước hoàn toàn MIỄN PHÍ của Windear hôm nay nhé."
      }
    };

    function appendMessage(text, sender, ctaType) {
      var msgDiv = document.createElement('div');
      msgDiv.className = 'chat-msg ' + sender;
      
      var bubbleDiv = document.createElement('div');
      bubbleDiv.className = 'msg-bubble';
      bubbleDiv.innerText = text;
      msgDiv.appendChild(bubbleDiv);

      if (ctaType === 'waitlist' || ctaType === 'buy') {
        var ctaBtn = document.createElement('button');
        ctaBtn.className = 'chat-cta-btn';
        ctaBtn.innerHTML = '🎁 Điền Form Danh Sách Chờ Ngay &rarr;';
        ctaBtn.onclick = function (e) {
          if (window.openWindearSurvey) window.openWindearSurvey(e);
        };
        msgDiv.appendChild(ctaBtn);
      } else if (ctaType === 'start') {
        var ctaBtn = document.createElement('button');
        ctaBtn.className = 'chat-cta-btn';
        ctaBtn.style.background = '#06B6D4';
        ctaBtn.innerHTML = '⚡ Bắt Đầu Luyện Nghe Miễn Phí &rarr;';
        ctaBtn.onclick = function (e) {
          if (window.openWindearSurvey) window.openWindearSurvey(e);
        };
        msgDiv.appendChild(ctaBtn);
      }

      messagesContainer.appendChild(msgDiv);
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function handleUserInput(queryText) {
      var text = (queryText || inputField.value).trim();
      if (!text) return;

      appendMessage(text, 'user');
      if (inputField) inputField.value = '';

      // Match query
      var lower = text.toLowerCase();
      var responseText = "";
      var ctaType = null;

      if (lower.indexOf('phí') !== -1 || lower.indexOf('tiền') !== -1 || lower.indexOf('free') !== -1 || lower.indexOf('mua') !== -1) {
        responseText = botScript.answers.free;
        ctaType = 'start';
      } else if (lower.indexOf('gốc') !== -1 || lower.indexOf('kém') !== -1 || lower.indexOf('khó') !== -1 || lower.indexOf('dở') !== -1) {
        responseText = botScript.answers.lost;
      } else if (lower.indexOf('bận') !== -1 || lower.indexOf('thời gian') !== -1 || lower.indexOf('phút') !== -1 || lower.indexOf('nhanh') !== -1) {
        responseText = botScript.answers.time;
      } else if (lower.indexOf('khác') !== -1 || lower.indexOf('ejoy') !== -1 || lower.indexOf('elsa') !== -1 || lower.indexOf('mochi') !== -1) {
        responseText = botScript.answers.diff;
      } else if (lower.indexOf('giọng') !== -1 || lower.indexOf('anh') !== -1 || lower.indexOf('úc') !== -1 || lower.indexOf('mỹ') !== -1) {
        responseText = botScript.answers.accents;
      } else if (lower.indexOf('bước') !== -1 || lower.indexOf('cách') !== -1 || lower.indexOf('phương pháp') !== -1) {
        responseText = botScript.answers.method;
      } else if (lower.indexOf('waitlist') !== -1 || lower.indexOf('form') !== -1 || lower.indexOf('đăng ký') !== -1 || lower.indexOf('quà') !== -1 || lower.indexOf('pro') !== -1) {
        responseText = botScript.answers.waitlist;
        ctaType = 'waitlist';
      } else {
        responseText = "Windear AI đã ghi nhận thắc mắc của bạn! Thật ra không cần tốn tiền hay thời gian đâu ạ. Bạn trải nghiệm ngay phương pháp 4 bước bóc tách audio hoàn toàn miễn phí của Windear hoặc giữ suất Waitlist nhận quà nhé!";
        ctaType = 'waitlist';
      }

      setTimeout(function () {
        appendMessage(responseText, 'bot', ctaType);
      }, 400);
    }

    window.triggerGreetingIfEmpty = function () {
      if (!isInitialized) {
        isInitialized = true;
        appendMessage(botScript.greeting, 'bot', 'start');
      }
    };

    if (closeBtn && chatWindow) {
      closeBtn.addEventListener('click', function () {
        chatWindow.classList.add('hidden');
        chatWindow.style.display = 'none';
        if (toggleBtn) {
          var iconOpen = toggleBtn.querySelector('.chat-icon-open');
          var iconClose = toggleBtn.querySelector('.chat-icon-close');
          if (iconOpen) iconOpen.style.display = 'block';
          if (iconClose) iconClose.style.display = 'none';
        }
      });
    }

    if (sendBtn) {
      sendBtn.addEventListener('click', function () {
        handleUserInput();
      });
    }

    if (inputField) {
      inputField.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          handleUserInput();
        }
      });
    }

    if (quickRepliesContainer) {
      quickRepliesContainer.addEventListener('click', function (e) {
        var target = e.target;
        if (target && target.classList.contains('chat-chip')) {
          var queryKey = target.getAttribute('data-query');
          var text = target.innerText;
          if (queryKey && botScript.answers[queryKey]) {
            appendMessage(text, 'user');
            var ctaType = (queryKey === 'waitlist' || queryKey === 'pro') ? 'waitlist' : (queryKey === 'free' ? 'start' : null);
            setTimeout(function () {
              appendMessage(botScript.answers[queryKey], 'bot', ctaType);
            }, 300);
          } else {
            handleUserInput(text);
          }
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWindear);
  } else {
    initWindear();
  }
})();

