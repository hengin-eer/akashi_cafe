<script>
  import Icon from "@iconify/svelte";

  // 現在の日付を取得
  const today = new Date();
  const todayString = today.toLocaleDateString("ja-JP", {
    year: "numeric",
    month: "long",
    day: "numeric",
    weekday: "long",
  });
</script>

<div class="home-container">
  <!-- ヘッダーセクション -->
  <header class="hero-section">
    <div class="hero-content">
      <h1 class="app-title">
        <Icon icon="ph:coffee" width="32" />
        明石高専 学生食堂
      </h1>
      <p class="hero-subtitle">今日のメニューをチェックしよう</p>
      <div class="date-info">
        <Icon icon="ph:calendar" width="20" />
        <span>{todayString}</span>
      </div>
    </div>
  </header>

  <!-- メインアクションカード -->
  <section class="quick-actions">
    <a href="/menu" class="action-card main-action">
      <div class="card-icon">
        <Icon icon="ph:fork-knife" width="48" />
      </div>
      <div class="card-content">
        <h2>今日のメニュー</h2>
        <p>A・Bセットの詳細を確認</p>
      </div>
      <div class="card-arrow">
        <Icon icon="ph:arrow-right" width="24" />
      </div>
    </a>
  </section>

  <!-- 機能カード -->
  <section class="feature-cards">
    <div class="card-grid">
      <!-- ログインカード -->
      <div class="feature-card">
        <div class="feature-icon">
          <Icon icon="ph:user-circle" width="32" />
        </div>
        <h3>ログイン</h3>
        <p>アカウントでログインして売り切れ情報を投稿</p>
        <a href="/login" class="feature-link">
          ログインページへ
          <Icon icon="ph:arrow-right" width="16" />
        </a>
      </div>

      <!-- 売り切れ情報カード -->
      <div class="feature-card">
        <div class="feature-icon sold-out">
          <Icon icon="ph:x-circle" width="32" />
        </div>
        <h3>売り切れ情報</h3>
        <p>リアルタイムで売り切れ状況をチェック</p>
        <div class="feature-link disabled">近日公開予定</div>
      </div>

      <!-- 栄養情報カード -->
      <div class="feature-card">
        <div class="feature-icon nutrition">
          <Icon icon="ph:heart" width="32" />
        </div>
        <h3>栄養情報</h3>
        <p>カロリーやアレルゲン情報を確認</p>
        <a href="/menu" class="feature-link">
          メニューで確認
          <Icon icon="ph:arrow-right" width="16" />
        </a>
      </div>
    </div>
  </section>

  <!-- お知らせセクション -->
  <section class="news-section">
    <h2 class="section-title">
      <Icon icon="ph:megaphone" width="24" />
      お知らせ
    </h2>
    <div class="news-list">
      <div class="news-item">
        <div class="news-date">
          <Icon icon="ph:calendar-dots" width="16" />
          2025年7月18日
        </div>
        <h4>システムリニューアルのお知らせ</h4>
        <p>
          学生食堂システムをリニューアルしました。新機能をお楽しみください。
        </p>
      </div>

      <div class="news-item">
        <div class="news-date">
          <Icon icon="ph:calendar-dots" width="16" />
          2025年7月15日
        </div>
        <h4>夏季メニューの提供開始</h4>
        <p>暑い夏にぴったりの冷たいメニューを追加しました。</p>
      </div>
    </div>
  </section>

  <!-- フッター情報 -->
  <footer class="home-footer">
    <div class="footer-content">
      <div class="footer-logo">
        <Icon icon="ph:coffee" width="24" />
        <span>明石高専 学生食堂システム</span>
      </div>
      <p class="footer-text">学生のみなさんの食事をサポートします</p>
    </div>
  </footer>
</div>

<style>
  .home-container {
    min-height: 100vh;
    padding: 1rem;
    max-width: 600px;
    margin: 0 auto;
  }

  /* ヒーローセクション */
  .hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
  }

  .hero-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .app-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
  }

  .hero-subtitle {
    margin: 0;
    font-size: 1rem;
    opacity: 0.9;
  }

  .date-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.2);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
  }

  /* クイックアクション */
  .quick-actions {
    margin-bottom: 2rem;
  }

  .action-card {
    display: flex;
    align-items: center;
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    text-decoration: none;
    color: inherit;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    border: 2px solid transparent;
  }

  .action-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    border-color: #007bff;
  }

  .card-icon {
    flex-shrink: 0;
    margin-right: 1rem;
    padding: 1rem;
    background: linear-gradient(135deg, #007bff, #0056b3);
    border-radius: 12px;
    color: white;
  }

  .card-content {
    flex-grow: 1;
  }

  .card-content h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1.3rem;
    font-weight: 600;
    color: #333;
  }

  .card-content p {
    margin: 0;
    color: #666;
    font-size: 0.9rem;
  }

  .card-arrow {
    flex-shrink: 0;
    margin-left: 1rem;
    color: #999;
    transition: all 0.3s ease;
  }

  .action-card:hover .card-arrow {
    color: #007bff;
    transform: translateX(4px);
  }

  /* 機能カード */
  .feature-cards {
    margin-bottom: 2rem;
  }

  .card-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .feature-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

  .feature-icon {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem auto;
    background: #e3f2fd;
    color: #007bff;
  }

  .feature-icon.sold-out {
    background: #ffebee;
    color: #dc3545;
  }

  .feature-icon.nutrition {
    background: #e8f5e8;
    color: #28a745;
  }

  .feature-card h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: #333;
  }

  .feature-card p {
    margin: 0 0 1rem 0;
    color: #666;
    font-size: 0.9rem;
    line-height: 1.5;
  }

  .feature-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: #007bff;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
    transition: color 0.2s;
  }

  .feature-link:hover {
    color: #0056b3;
  }

  .feature-link.disabled {
    color: #999;
    cursor: not-allowed;
  }

  /* お知らせセクション */
  .news-section {
    margin-bottom: 2rem;
  }

  .section-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.2rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
    color: #333;
  }

  .news-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .news-item {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .news-date {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #666;
    font-size: 0.8rem;
    margin-bottom: 0.5rem;
  }

  .news-item h4 {
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
    font-weight: 600;
    color: #333;
  }

  .news-item p {
    margin: 0;
    color: #666;
    font-size: 0.9rem;
    line-height: 1.5;
  }

  /* フッター */
  .home-footer {
    text-align: center;
    padding: 2rem 0;
    margin-top: 2rem;
  }

  .footer-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    font-weight: 600;
    color: #333;
    margin-bottom: 0.5rem;
  }

  .footer-text {
    margin: 0;
    color: #666;
    font-size: 0.9rem;
  }

  /* レスポンシブ */
  @media (min-width: 480px) {
    .card-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (min-width: 768px) {
    .home-container {
      max-width: 800px;
      padding: 2rem;
    }

    .card-grid {
      grid-template-columns: repeat(3, 1fr);
    }

    .hero-section {
      padding: 3rem;
    }

    .app-title {
      font-size: 2rem;
    }

    .hero-subtitle {
      font-size: 1.2rem;
    }
  }
</style>
