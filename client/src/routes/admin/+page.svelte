<script>
  import Icon from "@iconify/svelte";
</script>

<div class="container">
  <h1>管理者メニュー</h1>
  <p class="subtitle">明石カフェ管理システム</p>

  <div class="menu-grid">
    <!-- メニュー追加 -->
    <a href="/admin/menu/upload" class="menu-card upload-card">
      <div class="card-icon">
        <Icon icon="ph:upload" width="48" />
      </div>
      <div class="card-content">
        <h3>メニュー追加</h3>
        <p>CSVファイルをアップロードして日替わりメニューを一括登録できます</p>
        <div class="card-features">
          <span class="feature-tag">
            <Icon icon="ph:file-csv" width="16" />
            CSV対応
          </span>
          <span class="feature-tag">
            <Icon icon="ph:check-circle" width="16" />
            バリデーション
          </span>
        </div>
      </div>
      <div class="card-arrow">
        <Icon icon="ph:arrow-right" width="24" />
      </div>
    </a>

    <!-- メニュー管理 -->
    <a href="/admin/menu/list" class="menu-card manage-card">
      <div class="card-icon">
        <Icon icon="ph:list-checks" width="48" />
      </div>
      <div class="card-content">
        <h3>メニュー管理</h3>
        <p>登録済みの日替わりメニューの一覧表示・削除・検索ができます</p>
        <div class="card-features">
          <span class="feature-tag">
            <Icon icon="ph:funnel" width="16" />
            フィルター
          </span>
          <span class="feature-tag">
            <Icon icon="ph:trash" width="16" />
            一括削除
          </span>
        </div>
      </div>
      <div class="card-arrow">
        <Icon icon="ph:arrow-right" width="24" />
      </div>
    </a>
  </div>

  <!-- 統計情報 -->
  <div class="stats-section">
    <h2>システム情報</h2>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <Icon icon="ph:calendar" width="32" />
        </div>
        <div class="stat-content">
          <div class="stat-label">日替わりメニュー管理</div>
          <div class="stat-description">CSV形式でのメニュー登録と管理</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <Icon icon="ph:shield-check" width="32" />
        </div>
        <div class="stat-content">
          <div class="stat-label">データバリデーション</div>
          <div class="stat-description">アップロード時の自動検証機能</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <Icon icon="ph:users" width="32" />
        </div>
        <div class="stat-content">
          <div class="stat-label">ユーザーフレンドリー</div>
          <div class="stat-description">直感的で使いやすいインターフェース</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ヘルプセクション -->
  <div class="help-section">
    <h2>使い方ガイド</h2>
    <div class="help-grid">
      <div class="help-item">
        <div class="help-step">1</div>
        <div class="help-content">
          <h4>CSVファイルを準備</h4>
          <p>指定されたフォーマットでメニューデータを準備してください</p>
        </div>
      </div>

      <div class="help-item">
        <div class="help-step">2</div>
        <div class="help-content">
          <h4>メニュー追加でアップロード</h4>
          <p>CSVファイルを選択してアップロードボタンをクリック</p>
        </div>
      </div>

      <div class="help-item">
        <div class="help-step">3</div>
        <div class="help-content">
          <h4>メニュー管理で確認・削除</h4>
          <p>登録されたメニューの確認や不要なデータの削除が可能</p>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .container {
    padding: 0;
  }

  h1 {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    color: #333;
    text-align: center;
  }

  .subtitle {
    font-size: 1.1rem;
    color: #666;
    text-align: center;
    margin-bottom: 3rem;
  }

  /* メインメニュー */
  .menu-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 2rem;
    margin-bottom: 4rem;
  }

  .menu-card {
    display: flex;
    align-items: center;
    padding: 2rem;
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    text-decoration: none;
    color: inherit;
    transition: all 0.3s ease;
    border: 2px solid transparent;
  }

  .menu-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  }

  .upload-card:hover {
    border-color: #007bff;
    background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
  }

  .manage-card:hover {
    border-color: #28a745;
    background: linear-gradient(135deg, #f8fff9 0%, #ffffff 100%);
  }

  .card-icon {
    flex-shrink: 0;
    margin-right: 1.5rem;
    padding: 1rem;
    border-radius: 12px;
    color: white;
  }

  .upload-card .card-icon {
    background: linear-gradient(135deg, #007bff, #0056b3);
  }

  .manage-card .card-icon {
    background: linear-gradient(135deg, #28a745, #1e7e34);
  }

  .card-content {
    flex-grow: 1;
  }

  .card-content h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.4rem;
    font-weight: 600;
    color: #333;
  }

  .card-content p {
    margin: 0 0 1rem 0;
    color: #666;
    line-height: 1.5;
  }

  .card-features {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .feature-tag {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.5rem;
    background: #f8f9fa;
    border-radius: 12px;
    font-size: 0.8rem;
    color: #666;
  }

  .card-arrow {
    flex-shrink: 0;
    margin-left: 1rem;
    color: #999;
    transition: all 0.3s ease;
  }

  .menu-card:hover .card-arrow {
    color: #333;
    transform: translateX(4px);
  }

  /* 統計情報セクション */
  .stats-section {
    margin-bottom: 4rem;
  }

  .stats-section h2 {
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    color: #333;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .stat-card {
    display: flex;
    align-items: center;
    padding: 1.5rem;
    background: #f8f9fa;
    border-radius: 12px;
    border-left: 4px solid #007bff;
  }

  .stat-icon {
    flex-shrink: 0;
    margin-right: 1rem;
    color: #007bff;
  }

  .stat-content {
    flex-grow: 1;
  }

  .stat-label {
    font-weight: 600;
    margin-bottom: 0.25rem;
    color: #333;
  }

  .stat-description {
    font-size: 0.9rem;
    color: #666;
  }

  /* ヘルプセクション */
  .help-section h2 {
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    color: #333;
  }

  .help-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .help-item {
    display: flex;
    align-items: flex-start;
    padding: 1.5rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .help-step {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    background: #007bff;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    margin-right: 1rem;
  }

  .help-content h4 {
    margin: 0 0 0.5rem 0;
    font-weight: 600;
    color: #333;
  }

  .help-content p {
    margin: 0;
    color: #666;
    line-height: 1.5;
  }

  /* レスポンシブ */
  @media (max-width: 768px) {
    .container {
      padding: 1rem;
    }

    h1 {
      font-size: 2rem;
    }

    .menu-grid {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }

    .menu-card {
      flex-direction: column;
      text-align: center;
      padding: 1.5rem;
    }

    .card-icon {
      margin-right: 0;
      margin-bottom: 1rem;
    }

    .card-arrow {
      margin-left: 0;
      margin-top: 1rem;
    }

    .stats-grid,
    .help-grid {
      grid-template-columns: 1fr;
    }

    .stat-card,
    .help-item {
      padding: 1rem;
    }
  }

  @media (max-width: 480px) {
    .menu-grid {
      grid-template-columns: 1fr;
    }

    .menu-card {
      min-width: unset;
    }
  }
</style>
