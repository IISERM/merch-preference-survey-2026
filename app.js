/**
 * IISER Mohali Merch Survey 2026 - Client Application
 */

let surveyData = [];
let questionAnalysisData = [];
let currentFontScale = 16; // default px

// 1. Dark Mode Toggle Logic (YouTube Dark Grey Theme)
function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  updateThemeButtonIcon(newTheme);
}

function updateThemeButtonIcon(theme) {
  const btn = document.getElementById('themeToggleBtn');
  if (btn) {
    btn.innerHTML = theme === 'dark' ? '☀️' : '🌙';
    btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode');
  }
}

function initTheme() {
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeButtonIcon(savedTheme);
}

// 2. Accessibility Widget & Font Size Scaling
function toggleA11yPanel() {
  const panel = document.getElementById('a11yPanel');
  if (panel) {
    panel.classList.toggle('open');
  }
}

function changeFontSize(delta) {
  currentFontScale = Math.min(Math.max(currentFontScale + delta, 13), 22);
  document.documentElement.style.setProperty('--font-scale', `${currentFontScale}px`);
  localStorage.setItem('fontScale', currentFontScale);
}

function resetFontSize() {
  currentFontScale = 16;
  document.documentElement.style.setProperty('--font-scale', '16px');
  localStorage.setItem('fontScale', 16);
}

function initFontSize() {
  const savedScale = parseInt(localStorage.getItem('fontScale'), 10);
  if (savedScale && !isNaN(savedScale)) {
    currentFontScale = savedScale;
    document.documentElement.style.setProperty('--font-scale', `${currentFontScale}px`);
  }
}

// 3. Mobile Nav Tab Scroll Indicators & Arrow Action
function updateNavScrollCue() {
  const navBar = document.getElementById('navBar');
  const wrapper = document.getElementById('navWrapper');
  const arrow = document.getElementById('navScrollArrow');

  if (!navBar || !wrapper) return;

  const hasMoreRight = navBar.scrollWidth - navBar.scrollLeft - navBar.clientWidth > 10;

  if (hasMoreRight) {
    wrapper.classList.add('has-scroll-right');
    if (arrow) arrow.style.opacity = '1';
  } else {
    wrapper.classList.remove('has-scroll-right');
    if (arrow) arrow.style.opacity = '0.4';
  }
}

function scrollNavRight() {
  const navBar = document.getElementById('navBar');
  if (!navBar) return;
  
  const hasMoreRight = navBar.scrollWidth - navBar.scrollLeft - navBar.clientWidth > 10;
  if (hasMoreRight) {
    navBar.scrollBy({ left: 160, behavior: 'smooth' });
  } else {
    navBar.scrollTo({ left: 0, behavior: 'smooth' });
  }
}

// 4. URL Hash Routing & Tab Switching
const VALID_TABS = ['summary', 'detailed', 'charts', 'guidelines', 'explorer', 'downloads'];

function switchTab(tabId, updateHash = true) {
  if (!VALID_TABS.includes(tabId)) {
    tabId = 'summary';
  }

  const tabs = document.querySelectorAll('.tab-content');
  const buttons = document.querySelectorAll('.nav-btn');
  
  tabs.forEach(tab => tab.classList.remove('active'));
  buttons.forEach(btn => btn.classList.remove('active'));
  
  const targetTab = document.getElementById(`tab-${tabId}`);
  const targetBtn = document.getElementById(`nav-${tabId}`);
  
  if (targetTab) targetTab.classList.add('active');
  if (targetBtn) {
    targetBtn.classList.add('active');
    targetBtn.scrollIntoView({ behavior: 'smooth', inline: 'nearest', block: 'nearest' });
  }

  if (updateHash) {
    history.replaceState(null, '', `#${tabId}`);
  }
  
  setTimeout(updateNavScrollCue, 300);
}

function handleHashRouting() {
  const hash = window.location.hash.replace('#', '');
  if (hash && VALID_TABS.includes(hash)) {
    switchTab(hash, false);
  } else {
    switchTab('summary', false);
  }
}

// 5. Fetch and Render Survey JSON Data & Question Breakdown
async function initSurveyApp() {
  initTheme();
  initFontSize();
  handleHashRouting();

  window.addEventListener('hashchange', handleHashRouting);

  const navBar = document.getElementById('navBar');
  if (navBar) {
    navBar.addEventListener('scroll', updateNavScrollCue);
    window.addEventListener('resize', updateNavScrollCue);
    setTimeout(updateNavScrollCue, 200);
  }

  try {
    const [surveyResp, qResp] = await Promise.all([
      fetch('data/survey_data.json'),
      fetch('data/question_analysis.json')
    ]);
    
    surveyData = await surveyResp.json();
    questionAnalysisData = await qResp.json();

    renderResponses(surveyData);
    renderDetailedQuestions(questionAnalysisData);
  } catch (error) {
    console.error('Unable to load survey JSON data:', error);
  }
}

// Render Detailed Question-by-Question Analysis
function renderDetailedQuestions(qList) {
  const container = document.getElementById('detailedQuestionsContainer');
  if (!container || !qList || qList.length === 0) return;

  container.innerHTML = qList.map(q => {
    let statsHtml = '';
    
    if (q.stats) {
      statsHtml = '<ul class="info-list" style="margin-top:8px;">' + 
        Object.entries(q.stats).map(([key, val]) => {
          if (typeof val === 'object' && val !== null) {
            if ('count' in val && 'pct' in val) {
              return `<li><strong>${key}:</strong> ${val.count} responses (${val.pct}%)</li>`;
            } else {
              return `<li><strong>${key}:</strong> ` + Object.entries(val).map(([k, v]) => `${k}: ${v}`).join(' | ') + `</li>`;
            }
          }
          return `<li><strong>${key}:</strong> ${val}</li>`;
        }).join('') + 
      '</ul>';
    } else if (q.sample_responses) {
      statsHtml = '<p style="font-size:0.88rem; color:var(--text-muted);"><strong>Sample Community Responses:</strong></p>' +
        '<ul>' + q.sample_responses.map(r => `<li>"${r}"</li>`).join('') + '</ul>';
    } else if (q.turing_ideas || q.general_ideas) {
      const ideas = [...(q.turing_ideas || []), ...(q.general_ideas || [])];
      statsHtml = '<p style="font-size:0.88rem; color:var(--text-muted);"><strong>Key Design Concepts Suggested:</strong></p>' +
        '<ul>' + ideas.slice(0, 8).map(r => `<li>"${r}"</li>`).join('') + '</ul>';
    }

    return `
      <div style="padding: 14px 0; border-bottom: 1px solid var(--border-color);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
          <h3 style="margin:0; font-size:1.05rem;">[${q.question_id}] ${q.title}</h3>
          <span style="font-size:0.75rem; font-weight:600; color:var(--primary); background:var(--bg-color); border:1px solid var(--border-color); padding:2px 8px; border-radius:12px;">${q.type}</span>
        </div>
        ${statsHtml}
        ${q.insight ? `<div class="note-box" style="margin-top:8px;"><strong>Key Insight:</strong> ${q.insight}</div>` : ''}
      </div>
    `;
  }).join('');
}

// Render responses in mobile cards and desktop table
function renderResponses(dataList) {
  const cardsContainer = document.getElementById('mobileCardsContainer');
  const tableBody = document.getElementById('desktopTableBody');
  const countBadge = document.getElementById('resultCount');
  
  if (countBadge) {
    countBadge.textContent = `Showing ${dataList.length} responses`;
  }

  if (!dataList || dataList.length === 0) {
    if (cardsContainer) cardsContainer.innerHTML = '<div class="response-item-card">No matching survey responses.</div>';
    if (tableBody) tableBody.innerHTML = '<tr><td colspan="6">No matching survey responses.</td></tr>';
    return;
  }

  // 1. Mobile Cards HTML
  if (cardsContainer) {
    cardsContainer.innerHTML = dataList.map(item => {
      const id = item.Respondent_ID || '-';
      const batch = item['Your affiliation with institute?\n(batch or program, in case of students)'] || 'Unspecified';
      const fields = (item['Which area(s)/field(s) are you interested in?'] || '-').replace(/;/g, ', ');
      const merchYr = item['How many merch do you buy per year?'] ?? '-';
      const types = (item['Which type of merchandise are you most interested in purchasing?'] || '-').replace(/;/g, ', ');
      const wtp = item['What is the price you would be willing to pay for a "good" Sweatshirt?'] || '-';
      
      return `
        <div class="response-item-card">
          <div class="response-header">
            <span>Respondent #${id}</span>
            <span class="response-batch">${batch}</span>
          </div>
          <div class="response-row">
            <span class="response-label">Fields:</span> ${fields}
          </div>
          <div class="response-row">
            <span class="response-label">Interested In:</span> ${types}
          </div>
          <div class="response-row">
            <span class="response-label">T-shirt/Hoodie WTP:</span> ${wtp} | <span class="response-label">Buys/yr:</span> ${merchYr}
          </div>
        </div>
      `;
    }).join('');
  }

  // 2. Desktop Table HTML
  if (tableBody) {
    tableBody.innerHTML = dataList.map(item => {
      const id = item.Respondent_ID || '-';
      const batch = item['Your affiliation with institute?\n(batch or program, in case of students)'] || 'Unspecified';
      const fields = (item['Which area(s)/field(s) are you interested in?'] || '-').replace(/;/g, ', ');
      const merchYr = item['How many merch do you buy per year?'] ?? '-';
      const types = (item['Which type of merchandise are you most interested in purchasing?'] || '-').replace(/;/g, ', ');
      const wtp = item['What is the price you would be willing to pay for a "good" Sweatshirt?'] || '-';
      
      return `
        <tr>
          <td><strong>${id}</strong></td>
          <td>${batch}</td>
          <td>${fields}</td>
          <td>${merchYr}</td>
          <td>${types}</td>
          <td>${wtp}</td>
        </tr>
      `;
    }).join('');
  }
}

// Search and Filter Logic
function filterResponses() {
  const query = document.getElementById('searchQuery').value.toLowerCase().trim();
  const batchFilter = document.getElementById('batchFilterSelect').value;

  const filtered = surveyData.filter(item => {
    const batch = (item['Your affiliation with institute?\n(batch or program, in case of students)'] || '').toString();
    const fullText = JSON.stringify(item).toLowerCase();

    const matchesQuery = !query || fullText.includes(query);
    const matchesBatch = !batchFilter || batch.includes(batchFilter);

    return matchesQuery && matchesBatch;
  });

  renderResponses(filtered);
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', initSurveyApp);
