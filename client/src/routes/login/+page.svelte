<script>
  import Icon from "@iconify/svelte";

  // Googleログイン処理
  const handleGoogleLogin = () => {
    alert("Googleログイン処理をここに実装してください。");
  };

  // 管理者ログイン処理
  const handleAdminLogin = () => {
    // 管理者ページへリダイレクト
    window.location.href = "/admin";
  };
</script>

<div class="login-container">
  <!-- ヘッダー -->
  <header class="login-header">
    <div class="logo">
      <Icon icon="ph:coffee" width="40" />
      <h1>明石高専 学生食堂</h1>
    </div>
    <p class="header-subtitle">アカウントにログインしてください</p>
  </header>

  <!-- ログインフォーム -->
  <section class="login-section">
    <!-- ユーザーログイン -->
    <div class="login-card">
      <div class="card-icon user">
        <Icon icon="ph:user-circle" width="32" />
      </div>
      <h2>学生ログイン</h2>
      <p class="card-description">
        学生アカウントでログインして売り切れ情報の投稿や、パーソナライズされた機能をご利用ください
      </p>

      <div class="benefits">
        <h4>
          <Icon icon="ph:check-circle" width="20" />
          ログインのメリット
        </h4>
        <ul>
          <li>売り切れ情報の投稿</li>
          <li>認証ユーザーとして信頼性向上</li>
          <li>お気に入りメニューの保存</li>
          <li>通知機能の利用</li>
        </ul>
      </div>

      <button class="login-button google" on:click={handleGoogleLogin}>
        <img
          src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
          alt="Googleアイコン"
          width="20"
          height="20"
        />
        Googleでログイン
      </button>
    </div>

    <!-- 管理者ログイン -->
    <div class="login-card admin">
      <div class="card-icon admin">
        <Icon icon="ph:shield-check" width="32" />
      </div>
      <h2>管理者ログイン</h2>
      <p class="card-description">
        管理者アカウントでメニューの追加・削除などの管理機能をご利用ください
      </p>

      <div class="admin-features">
        <h4>
          <Icon icon="ph:gear" width="20" />
          管理機能
        </h4>
        <ul>
          <li>メニューの追加・削除</li>
          <li>CSVファイルの一括アップロード</li>
          <li>売り切れ情報の管理</li>
          <li>システム設定</li>
        </ul>
      </div>

      <button class="login-button admin" on:click={handleAdminLogin}>
        <Icon icon="ph:sign-in" width="20" />
        管理者ページへ
      </button>
    </div>
  </section>

  <!-- 注意事項 -->
  <section class="notice-section">
    <div class="notice-card">
      <div class="notice-icon">
        <Icon icon="ph:info" width="24" />
      </div>
      <div class="notice-content">
        <h4>ご利用について</h4>
        <ul>
          <li>学生ログインにはGoogleアカウントが必要です</li>
          <li>管理者機能は許可されたユーザーのみご利用いただけます</li>
          <li>適切な利用をお心がけください</li>
        </ul>
      </div>
    </div>
  </section>
</div>

<style>
  .login-container {
    min-height: 100vh;
    padding: 1rem;
    max-width: 600px;
    margin: 0 auto;
  }

  /* ヘッダー */
  .login-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .logo {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .logo h1 {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
    color: #333;
  }

  .header-subtitle {
    margin: 0;
    color: #666;
    font-size: 0.9rem;
  }

  /* ログインセクション */
  .login-section {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .login-card {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

  .card-icon {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem auto;
    color: white;
  }

  .card-icon.user {
    background: linear-gradient(135deg, #007bff, #0056b3);
  }

  .card-icon.admin {
    background: linear-gradient(135deg, #28a745, #1e7e34);
  }

  .login-card h2 {
    font-size: 1.3rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    color: #333;
  }

  .card-description {
    margin: 0 0 1.5rem 0;
    color: #666;
    font-size: 0.9rem;
    line-height: 1.5;
  }

  /* ベネフィット・機能リスト */
  .benefits,
  .admin-features {
    text-align: left;
    margin-bottom: 1.5rem;
    background: #f8f9fa;
    border-radius: 8px;
    padding: 1rem;
  }

  .benefits h4,
  .admin-features h4 {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    font-weight: 600;
    margin: 0 0 0.75rem 0;
    color: #333;
  }

  .benefits ul,
  .admin-features ul {
    margin: 0;
    padding-left: 1.25rem;
  }

  .benefits li,
  .admin-features li {
    margin-bottom: 0.25rem;
    font-size: 0.85rem;
    color: #666;
    line-height: 1.4;
  }

  /* ログインボタン */
  .login-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    width: 100%;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    color: white;
  }

  .login-button.google {
    background: #4285f4;
    box-shadow: 0 2px 4px rgba(66, 133, 244, 0.3);
  }

  .login-button.google:hover {
    background: #3367d6;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(66, 133, 244, 0.4);
  }

  .login-button.admin {
    background: linear-gradient(135deg, #28a745, #1e7e34);
    box-shadow: 0 2px 4px rgba(40, 167, 69, 0.3);
  }

  .login-button.admin:hover {
    background: linear-gradient(135deg, #218838, #1a6b2d);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(40, 167, 69, 0.4);
  }

  /* 注意事項セクション */
  .notice-section {
    margin-top: 2rem;
  }

  .notice-card {
    display: flex;
    gap: 1rem;
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .notice-icon {
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    background: #e3f2fd;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #007bff;
  }

  .notice-content h4 {
    margin: 0 0 0.75rem 0;
    font-size: 1rem;
    font-weight: 600;
    color: #333;
  }

  .notice-content ul {
    margin: 0;
    padding-left: 1.25rem;
    color: #666;
  }

  .notice-content li {
    margin-bottom: 0.25rem;
    font-size: 0.9rem;
    line-height: 1.4;
  }

  /* レスポンシブ */
  @media (min-width: 768px) {
    .login-container {
      padding: 2rem;
      max-width: 800px;
    }

    .login-section {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 2rem;
    }

    .logo {
      flex-direction: row;
    }

    .logo h1 {
      font-size: 1.8rem;
    }
  }
</style>
